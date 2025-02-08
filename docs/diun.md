# Diun

To use the Diun proxy, you need to have a Diun instance running. Diun is a Docker image update notifier service written
in Go. It can watch multiple Docker registries and send notifications to multiple messaging platforms, including Slack,
Discord, Telegram, and more.

## Configuration

Follow the instruction on the <a href="https://crazymax.dev/diun/notif/webhook/" target="_blank">Diun website</a> to set
up a webhook in Diun. The endpoint URL needs to point to the `/feeds/{feed_id}/diun` endpoint of your Webhook Feeds
instance.

The `feed_id` is the `id` of the feed that you want to add the feed item to.
