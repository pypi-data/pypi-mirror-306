import amsdal_glue as glue
from amsdal_data.application import DataApplication
from amsdal_data.transactions.decorators import transaction
from amsdal_data.transactions.errors import AmsdalTransactionError
from amsdal_models.classes.manager import ClassManager
from amsdal_models.querysets.executor import LAKEHOUSE_DB_ALIAS


@transaction
def rollback_to_timestamp(timestamp: float) -> None:
    """
    Rollback the data to the given timestamp
    Args:
        timestamp (float): The timestamp to rollback the data to.
    Returns:
        None
    """
    class_manager = ClassManager()

    lakehouse_connection = (
        DataApplication()._application.lakehouse_connection_manager.get_connection_pool('Company').get_connection()
    )

    metadatas_to_delete = lakehouse_connection.query(
        query=glue.QueryStatement(
            table=glue.SchemaReference(name='Metadata', version=glue.Version.LATEST),
            where=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='updated_at'), table_name='Metadata'),
                    lookup=glue.FieldLookup.GT,
                    value=glue.Value(timestamp),
                ),
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='prior_version'), table_name='Metadata'),
                    lookup=glue.FieldLookup.ISNULL,
                    value=glue.Value(True),
                ),
            ),
        )
    )

    ids_to_ignore = [m.data['address']['object_id'] for m in metadatas_to_delete]

    metadatas_to_revert = lakehouse_connection.query(
        query=glue.QueryStatement(
            table=glue.SchemaReference(name='Metadata', version=glue.Version.LATEST),
            where=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='updated_at'), table_name='Metadata'),
                    lookup=glue.FieldLookup.GT,
                    value=glue.Value(timestamp),
                ),
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='prior_version'), table_name='Metadata'),
                    lookup=glue.FieldLookup.ISNULL,
                    value=glue.Value(False),
                ),
            ),
        )
    )

    transaction_ids = {m.data['transaction']['object_id'] for m in metadatas_to_revert}
    transaction_ids.update({m.data['transaction']['object_id'] for m in metadatas_to_delete})
    ids_to_revert = [
        (m.data['address']['object_id'], m.data['address']['class_name'])
        for m in metadatas_to_revert
        if m.data['address']['object_id'] not in ids_to_ignore
    ]

    if transaction_ids:
        _conditions = []
        for transaction_id in transaction_ids:
            _parent_field = glue.Field(name='transaction')
            _child_field = glue.Field(name='object_id', parent=_parent_field)
            _parent_field.child = _child_field
            _conditions.append(
                glue.Condition(
                    field=glue.FieldReference(field=_parent_field, table_name='Metadata'),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(transaction_id),
                )
            )

        conflict_metadata = lakehouse_connection.query(
            query=glue.QueryStatement(
                table=glue.SchemaReference(name='Metadata', version=glue.Version.LATEST),
                where=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(field=glue.Field(name='updated_at'), table_name='Metadata'),
                        lookup=glue.FieldLookup.LTE,
                        value=glue.Value(timestamp),
                    ),
                    glue.Conditions(*_conditions, connector=glue.FilterConnector.OR),
                ),
            )
        )
        if conflict_metadata:
            # print(timestamp)
            # print(conflict_metadata)
            # input('conflict')
            msg = 'Cannot rollback to this timestamp because it will conflict with other transactions'
            raise AmsdalTransactionError(msg)

    for m in metadatas_to_delete:
        address = m.data['address']
        class_name = address['class_name']
        schema_type = class_manager.resolve_schema_type(class_name)

        model_class = class_manager.import_model_class(class_name, schema_type)
        obj = (
            model_class.objects.filter(_address__object_id=address['object_id'])
            .using(LAKEHOUSE_DB_ALIAS)
            .latest()
            .first()
            .execute()
        )

        if obj and not obj.get_metadata().is_deleted:
            obj.delete()

    for object_id, class_name in ids_to_revert:
        schema_type = class_manager.resolve_schema_type(class_name)
        model_class = class_manager.import_model_class(class_name, schema_type)

        obj = (
            model_class.objects.filter(_address__object_id=object_id)
            .using(LAKEHOUSE_DB_ALIAS)
            .latest()
            .first()
            .execute()
        )
        old_obj = (
            model_class.objects.filter(_address__object_id=object_id, _metadata__updated_at__lte=timestamp)
            .using(LAKEHOUSE_DB_ALIAS)
            .order_by('-_metadata__updated_at')
            .first()
            .execute()
        )

        if obj and old_obj:
            for field, value in old_obj.model_dump().items():
                setattr(obj, field, value)

            obj.get_metadata().is_deleted = old_obj.get_metadata().is_deleted

            obj.save()


@transaction
def rollback_transaction(transaction_id: str) -> None:
    """
    Rollback the data to the point in time before the given transaction
    Args:
        transaction_id (str): The transaction ID to rollback the data to.
    Returns:
        None
    """

    lakehouse_connection = (
        DataApplication()._application.lakehouse_connection_manager.get_connection_pool('Company').get_connection()
    )

    _parent_field = glue.Field(name='transaction')
    _child_field = glue.Field(name='object_id', parent=_parent_field)
    _parent_field.child = _child_field

    metadatas_to_revert = lakehouse_connection.query(
        query=glue.QueryStatement(
            table=glue.SchemaReference(name='Metadata', version=glue.Version.LATEST),
            where=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=_parent_field, table_name='Metadata'),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(transaction_id),
                )
            ),
            order_by=[
                glue.OrderByQuery(
                    field=glue.FieldReference(field=glue.Field(name='updated_at'), table_name='Metadata'),
                    direction=glue.OrderDirection.DESC,
                )
            ],
        )
    )

    if not metadatas_to_revert:
        msg = 'Transaction not found'
        raise AmsdalTransactionError(msg)
    updated_at = metadatas_to_revert[0].data['updated_at']

    rollback_to_timestamp(updated_at)
