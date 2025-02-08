# Templates

Templates are used to generate the final output of the title and description of a feed item. They are written in
the [Jinja2](http://jinja.pocoo.org/docs/2.10/) templating language.

## Custom templates

Templates have the following naming convention:

`{proxy}.title.jinja2`

`{proxy}.description.jinja2`

Where `{proxy}` is the name of the proxy that the template is for.

### Custom template for a proxy

To use your own templates for feed items, you can create a new file in the `templates/custom/` folder. This template
will be used for all feed items for the specified proxy.

#### Example

For the `diun` proxy, you would create a file named `diun.title.jinja2` in the `templates/custom/` folder.

### Custom template for a feed

If you want more fine-grained control over the templates, you can create a custom template for a specific feed by
creating the template in a subfolder of `templates/custom/` named after the feed's `id`.

#### Example

For the `diun` proxy with the feed id `e3d19c27-4e68-4d51-bcae-63f5b971d8ab`, you would create a file named
`diun.title.jinja2` in the `templates/custom/e3d19c27-4e68-4d51-bcae-63f5b971d8ab/` folder.
