import urllib.parse

from fastapi import Query
from fastapi import Request

from amsdal_server.apps.common.serializers.objects_response import ObjectsResponse
from amsdal_server.apps.objects.router import router
from amsdal_server.apps.objects.services.object_versions_api import ObjectVersionsApi


@router.get('/api/objects/{address:path}/')
async def object_detail(
    address: str,
    request: Request,
    version_id: str = '',
    *,
    all_versions: bool = False,
    include_metadata: bool = True,
    file_optimized: bool = False,
    select_related: str | None = Query(
        default=None,
        description='Comma-separated list of related fields to fetch',
        examples=['field1', 'field1,field2'],
    ),
) -> ObjectsResponse:
    _select_related = select_related.split(',') if select_related else None

    return ObjectVersionsApi.get_object_versions(
        request.user,
        base_url=str(request.base_url),
        address=urllib.parse.unquote(address),
        version_id=version_id,
        all_versions=all_versions,
        include_metadata=include_metadata,
        file_optimized=file_optimized,
        select_related=_select_related,
    )
