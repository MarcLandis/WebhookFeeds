# Add feed items

Usually there should be no need to add feed items manually, as they are added through the [proxy](what_is_proxy.md)
endpoint. However, if you want to add feed items manually, you can do so using the OpenAPI UI.

1. Open the OpenAPI UI by navigating to `/docs` in your browser.
2. Click on the `POST /feeds/{feed_id}/items` endpoint.
3. Click on the `Try it out` button.
4. Fill in the required fields. The `feed_id` is the `id` of the feed that you want to add the feed item to.
5. Click on the `Execute` button.
6. The feed item will be added, and you will receive a response with the feed item data.
