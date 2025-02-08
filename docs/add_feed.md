# Add a feed

Currently, it is only possible to add feeds using the OpenAPI UI. This will be improved in the future.

1. Open the OpenAPI UI by navigating to `/docs` in your browser.
2. Click on the `POST /feeds` endpoint.
3. Click on the `Try it out` button.
4. Fill in the required fields.
5. Click on the `Execute` button.
6. The feed will be added, and you will receive a response with the feed data.

In the response body, you will see the feed data, including the `id` of the feed. You will need this `id` to add feed
items to the feed.

If you want to get the `id` of a feed that you have already added, you can do so by navigating to the `GET /feeds`
endpoint in the OpenAPI UI and click on the `Try it out` followed by the `Execute` button. You will see a list of all the feeds that you have
added, including their `id`s.
