# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal

import httpx

from ..types import index_create_params, index_search_params, index_finetune_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.index_get_response import IndexGetResponse
from ..types.index_list_response import IndexListResponse
from ..types.index_create_response import IndexCreateResponse
from ..types.index_delete_response import IndexDeleteResponse
from ..types.index_search_response import IndexSearchResponse
from ..types.index_status_response import IndexStatusResponse
from ..types.index_finetune_response import IndexFinetuneResponse
from ..types.index_status_by_type_response import IndexStatusByTypeResponse

__all__ = ["IndexesResource", "AsyncIndexesResource"]


class IndexesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IndexesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/objective-inc/objective-python#accessing-raw-response-data-eg-headers
        """
        return IndexesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IndexesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/objective-inc/objective-python#with_streaming_response
        """
        return IndexesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        configuration: index_create_params.Configuration,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexCreateResponse:
        """
        Creates an Index.

        Indexes are created with unique IDs like `idx_rHlXLhCTma74w1E_xbRXl`. These IDs
        are unique and cannot be changed. In a future release we will be adding the
        ability to alias Indexes, supporting names.

        This is an asynchronous operation.

        ## Index configuration

        ### Index types

        Indexes have an index type that determines how the data inserted is processed.

        We currently support 5 Index types:

        1. text - semantically search text through the optimized combination of
           lexical/keyword and neural search capabilities that leverage state-of-the-art
           embeddings.
        2. multimodal - combines lexical/keyword search and neural search for both text
           and image data. Enables searching over text and images with both keyword
           precision and semantic understanding.
        3. image - semantically search images with text using image embeddings for
           search.
        4. text-neural - semantically search text content using state of the art text
           embeddings for search.
        5. multimodal-neural - semantically search text AND image content using
           multimodal embeddings for search.

        ### Indexing fields from Objects

        Indexes support configuring how fields in Objects that are indexed are
        processed. The following configurations are supported at a field level:

        1. Crawlable - fields which will be crawled and made available for search. Read
           more about [crawling](/apis/ingestion/crawling).
        2. Searchable - fields which will contribute to search relevance.
        3. Filterable - fields which may be filtered upon. Read more about
           [filtering](/apis/search/overview#filtering-search-results).
        4. Types - A mapping of fields to data types for filterable fields. By default
           all filterable fields are considered strings, unless specified here. For more
           info on supported types see
           [field types](/apis/search/filtering#field-types).

        **Defaults:**

        1. Crawlable - no fields are crawled
        2. Filterable - no fields are filterable

        ### Finetuning

        Indexes can learn from your feedback, training your index to retrieve more
        relevant results that better match your unique business needs. To configure
        `finetuning` set your base index using `base_index_id` and provide `feedback` in
        the form of `query`, `object_id`, and `label`. Check out the Quickstart guide to
        get started.

        Acceptable labels are:

        - **GREAT**: For objects that you want to encourage retrieving for the specified
          query.
        - **OK**: For objects that have a loose connection to the query but you do not
          want to reward.
        - **BAD**: For objects that you want to discourage retrieving for the specified
          query.

        Constraints:

        - You must include at least 50 queries
        - Each query must have at least one object with a “GREAT” label and one object
          with a “BAD” label.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/indexes",
            body=maybe_transform({"configuration": configuration}, index_create_params.IndexCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexCreateResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexListResponse:
        """Get Indexes"""
        return self._get(
            "/indexes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexListResponse,
        )

    def delete(
        self,
        index_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexDeleteResponse:
        """Schedules an Index for deletion.

        This is an asynchronous operation.

        If no such Index exists, this does nothing.

        Search results and other APIs are cached for several minutes not just by this
        API but possibly by third-party servers out of our control. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
        regarding the standard HTTP caching mechanism that we use to improve
        performance.

        Returns a JSON object with the ID of the deleted Index.

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return self._delete(
            f"/indexes/{index_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexDeleteResponse,
        )

    def finetune(
        self,
        index_id: str,
        *,
        feedback: Iterable[index_finetune_params.Feedback],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexFinetuneResponse:
        """Finetune a base index given feedback.

        Read more about finetuning in our
        [docs](https://www.objective.inc/docs/quality/finetuning).

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return self._post(
            f"/indexes/{index_id}:finetune",
            body=maybe_transform({"feedback": feedback}, index_finetune_params.IndexFinetuneParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexFinetuneResponse,
        )

    def get(
        self,
        index_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexGetResponse:
        """Get Index by ID

        This is an asynchronous operation.

        If no such Index exists, it will return
        a 404.

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return self._get(
            f"/indexes/{index_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexGetResponse,
        )

    def search(
        self,
        index_id: str,
        *,
        filter_query: str | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        object_fields: str | NotGiven = NOT_GIVEN,
        offset: float | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        ranking_expr: str | NotGiven = NOT_GIVEN,
        relevance_cutoff: str | NotGiven = NOT_GIVEN,
        result_fields: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexSearchResponse:
        """
        Search for a query in an index

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return self._get(
            f"/indexes/{index_id}/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "filter_query": filter_query,
                        "limit": limit,
                        "object_fields": object_fields,
                        "offset": offset,
                        "query": query,
                        "ranking_expr": ranking_expr,
                        "relevance_cutoff": relevance_cutoff,
                        "result_fields": result_fields,
                    },
                    index_search_params.IndexSearchParams,
                ),
            ),
            cast_to=IndexSearchResponse,
        )

    def status(
        self,
        index_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexStatusResponse:
        """
        Get an index's status by ID.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return self._get(
            f"/indexes/{index_id}/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexStatusResponse,
        )

    def status_by_type(
        self,
        index_status_type: Literal["UPLOADED", "PROCESSING", "READY", "ERROR", "INCOMPLETE"],
        *,
        index_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexStatusByTypeResponse:
        """
        Get an index's status by ID and status type.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          index_id: Index ID

          index_status_type: Index Status Type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        if not index_status_type:
            raise ValueError(f"Expected a non-empty value for `index_status_type` but received {index_status_type!r}")
        return self._get(
            f"/indexes/{index_id}/status/{index_status_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexStatusByTypeResponse,
        )


class AsyncIndexesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIndexesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/objective-inc/objective-python#accessing-raw-response-data-eg-headers
        """
        return AsyncIndexesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIndexesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/objective-inc/objective-python#with_streaming_response
        """
        return AsyncIndexesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        configuration: index_create_params.Configuration,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexCreateResponse:
        """
        Creates an Index.

        Indexes are created with unique IDs like `idx_rHlXLhCTma74w1E_xbRXl`. These IDs
        are unique and cannot be changed. In a future release we will be adding the
        ability to alias Indexes, supporting names.

        This is an asynchronous operation.

        ## Index configuration

        ### Index types

        Indexes have an index type that determines how the data inserted is processed.

        We currently support 5 Index types:

        1. text - semantically search text through the optimized combination of
           lexical/keyword and neural search capabilities that leverage state-of-the-art
           embeddings.
        2. multimodal - combines lexical/keyword search and neural search for both text
           and image data. Enables searching over text and images with both keyword
           precision and semantic understanding.
        3. image - semantically search images with text using image embeddings for
           search.
        4. text-neural - semantically search text content using state of the art text
           embeddings for search.
        5. multimodal-neural - semantically search text AND image content using
           multimodal embeddings for search.

        ### Indexing fields from Objects

        Indexes support configuring how fields in Objects that are indexed are
        processed. The following configurations are supported at a field level:

        1. Crawlable - fields which will be crawled and made available for search. Read
           more about [crawling](/apis/ingestion/crawling).
        2. Searchable - fields which will contribute to search relevance.
        3. Filterable - fields which may be filtered upon. Read more about
           [filtering](/apis/search/overview#filtering-search-results).
        4. Types - A mapping of fields to data types for filterable fields. By default
           all filterable fields are considered strings, unless specified here. For more
           info on supported types see
           [field types](/apis/search/filtering#field-types).

        **Defaults:**

        1. Crawlable - no fields are crawled
        2. Filterable - no fields are filterable

        ### Finetuning

        Indexes can learn from your feedback, training your index to retrieve more
        relevant results that better match your unique business needs. To configure
        `finetuning` set your base index using `base_index_id` and provide `feedback` in
        the form of `query`, `object_id`, and `label`. Check out the Quickstart guide to
        get started.

        Acceptable labels are:

        - **GREAT**: For objects that you want to encourage retrieving for the specified
          query.
        - **OK**: For objects that have a loose connection to the query but you do not
          want to reward.
        - **BAD**: For objects that you want to discourage retrieving for the specified
          query.

        Constraints:

        - You must include at least 50 queries
        - Each query must have at least one object with a “GREAT” label and one object
          with a “BAD” label.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/indexes",
            body=await async_maybe_transform({"configuration": configuration}, index_create_params.IndexCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexCreateResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexListResponse:
        """Get Indexes"""
        return await self._get(
            "/indexes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexListResponse,
        )

    async def delete(
        self,
        index_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexDeleteResponse:
        """Schedules an Index for deletion.

        This is an asynchronous operation.

        If no such Index exists, this does nothing.

        Search results and other APIs are cached for several minutes not just by this
        API but possibly by third-party servers out of our control. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
        regarding the standard HTTP caching mechanism that we use to improve
        performance.

        Returns a JSON object with the ID of the deleted Index.

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return await self._delete(
            f"/indexes/{index_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexDeleteResponse,
        )

    async def finetune(
        self,
        index_id: str,
        *,
        feedback: Iterable[index_finetune_params.Feedback],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexFinetuneResponse:
        """Finetune a base index given feedback.

        Read more about finetuning in our
        [docs](https://www.objective.inc/docs/quality/finetuning).

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return await self._post(
            f"/indexes/{index_id}:finetune",
            body=await async_maybe_transform({"feedback": feedback}, index_finetune_params.IndexFinetuneParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexFinetuneResponse,
        )

    async def get(
        self,
        index_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexGetResponse:
        """Get Index by ID

        This is an asynchronous operation.

        If no such Index exists, it will return
        a 404.

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return await self._get(
            f"/indexes/{index_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexGetResponse,
        )

    async def search(
        self,
        index_id: str,
        *,
        filter_query: str | NotGiven = NOT_GIVEN,
        limit: float | NotGiven = NOT_GIVEN,
        object_fields: str | NotGiven = NOT_GIVEN,
        offset: float | NotGiven = NOT_GIVEN,
        query: str | NotGiven = NOT_GIVEN,
        ranking_expr: str | NotGiven = NOT_GIVEN,
        relevance_cutoff: str | NotGiven = NOT_GIVEN,
        result_fields: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexSearchResponse:
        """
        Search for a query in an index

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return await self._get(
            f"/indexes/{index_id}/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "filter_query": filter_query,
                        "limit": limit,
                        "object_fields": object_fields,
                        "offset": offset,
                        "query": query,
                        "ranking_expr": ranking_expr,
                        "relevance_cutoff": relevance_cutoff,
                        "result_fields": result_fields,
                    },
                    index_search_params.IndexSearchParams,
                ),
            ),
            cast_to=IndexSearchResponse,
        )

    async def status(
        self,
        index_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexStatusResponse:
        """
        Get an index's status by ID.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          index_id: Index ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        return await self._get(
            f"/indexes/{index_id}/status",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexStatusResponse,
        )

    async def status_by_type(
        self,
        index_status_type: Literal["UPLOADED", "PROCESSING", "READY", "ERROR", "INCOMPLETE"],
        *,
        index_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexStatusByTypeResponse:
        """
        Get an index's status by ID and status type.

        ## Status

        Objects within an index can have 4 different status types.

        1. `UPLOADED` - The state of an object that is in the object store but is
           pending processing.
        2. `PROCESSING` - The state of an object that is currently being indexed.
        3. `READY` - The state of an object that is live and searchable.
        4. `ERROR` - The state of an object that has encountered errors during
           processing; you can find out more information about the error by using the
           object status API.

        Args:
          index_id: Index ID

          index_status_type: Index Status Type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not index_id:
            raise ValueError(f"Expected a non-empty value for `index_id` but received {index_id!r}")
        if not index_status_type:
            raise ValueError(f"Expected a non-empty value for `index_status_type` but received {index_status_type!r}")
        return await self._get(
            f"/indexes/{index_id}/status/{index_status_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IndexStatusByTypeResponse,
        )


class IndexesResourceWithRawResponse:
    def __init__(self, indexes: IndexesResource) -> None:
        self._indexes = indexes

        self.create = to_raw_response_wrapper(
            indexes.create,
        )
        self.list = to_raw_response_wrapper(
            indexes.list,
        )
        self.delete = to_raw_response_wrapper(
            indexes.delete,
        )
        self.finetune = to_raw_response_wrapper(
            indexes.finetune,
        )
        self.get = to_raw_response_wrapper(
            indexes.get,
        )
        self.search = to_raw_response_wrapper(
            indexes.search,
        )
        self.status = to_raw_response_wrapper(
            indexes.status,
        )
        self.status_by_type = to_raw_response_wrapper(
            indexes.status_by_type,
        )


class AsyncIndexesResourceWithRawResponse:
    def __init__(self, indexes: AsyncIndexesResource) -> None:
        self._indexes = indexes

        self.create = async_to_raw_response_wrapper(
            indexes.create,
        )
        self.list = async_to_raw_response_wrapper(
            indexes.list,
        )
        self.delete = async_to_raw_response_wrapper(
            indexes.delete,
        )
        self.finetune = async_to_raw_response_wrapper(
            indexes.finetune,
        )
        self.get = async_to_raw_response_wrapper(
            indexes.get,
        )
        self.search = async_to_raw_response_wrapper(
            indexes.search,
        )
        self.status = async_to_raw_response_wrapper(
            indexes.status,
        )
        self.status_by_type = async_to_raw_response_wrapper(
            indexes.status_by_type,
        )


class IndexesResourceWithStreamingResponse:
    def __init__(self, indexes: IndexesResource) -> None:
        self._indexes = indexes

        self.create = to_streamed_response_wrapper(
            indexes.create,
        )
        self.list = to_streamed_response_wrapper(
            indexes.list,
        )
        self.delete = to_streamed_response_wrapper(
            indexes.delete,
        )
        self.finetune = to_streamed_response_wrapper(
            indexes.finetune,
        )
        self.get = to_streamed_response_wrapper(
            indexes.get,
        )
        self.search = to_streamed_response_wrapper(
            indexes.search,
        )
        self.status = to_streamed_response_wrapper(
            indexes.status,
        )
        self.status_by_type = to_streamed_response_wrapper(
            indexes.status_by_type,
        )


class AsyncIndexesResourceWithStreamingResponse:
    def __init__(self, indexes: AsyncIndexesResource) -> None:
        self._indexes = indexes

        self.create = async_to_streamed_response_wrapper(
            indexes.create,
        )
        self.list = async_to_streamed_response_wrapper(
            indexes.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            indexes.delete,
        )
        self.finetune = async_to_streamed_response_wrapper(
            indexes.finetune,
        )
        self.get = async_to_streamed_response_wrapper(
            indexes.get,
        )
        self.search = async_to_streamed_response_wrapper(
            indexes.search,
        )
        self.status = async_to_streamed_response_wrapper(
            indexes.status,
        )
        self.status_by_type = async_to_streamed_response_wrapper(
            indexes.status_by_type,
        )
