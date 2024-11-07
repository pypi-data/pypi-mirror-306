from typing import Any

from fastapi import Depends
from fastapi import Query
from fastapi import Request

from amsdal_server.apps.common.depends import get_fields_restrictions
from amsdal_server.apps.common.depends import get_filters
from amsdal_server.apps.common.serializers.fields_restriction import FieldsRestriction
from amsdal_server.apps.common.serializers.filter import Filter
from amsdal_server.apps.common.serializers.objects_response import ObjectsResponse
from amsdal_server.apps.objects.router import router
from amsdal_server.apps.objects.services.object_list_api import ObjectListApi


@router.get('/api/objects/', response_model_exclude_none=True, response_model=ObjectsResponse)
async def object_list(
    request: Request,
    class_name: str,
    *,
    include_metadata: bool = True,
    include_subclasses: bool = False,
    load_references: bool = False,
    all_versions: bool = False,
    file_optimized: bool = False,
    fields_restrictions: dict[str, FieldsRestriction] = Depends(get_fields_restrictions),
    filters: list[Filter] = Depends(get_filters),
    page: int = 1,
    page_size: int | None = Query(default=None),
    ordering: list[str] | None = Query(default=None),
    select_related: str | None = Query(
        default=None,
        description='Comma-separated list of related fields to fetch',
        examples=['field1', 'field1,field2'],
    ),
) -> dict[str, Any]:
    _select_related = select_related.split(',') if select_related else None

    return ObjectListApi.fetch_objects(
        request.user,
        base_url=str(request.base_url),
        class_name=class_name,
        filters=filters,
        fields_restrictions=fields_restrictions,
        include_metadata=include_metadata,
        include_subclasses=include_subclasses,
        load_references=load_references,
        all_versions=all_versions,
        file_optimized=file_optimized,
        page=page,
        page_size=page_size,
        ordering=ordering,
        select_related=_select_related,
    ).model_dump()
