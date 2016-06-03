import click
from graphql import parse
from graphql.language.parser import parse
from graphql.language.source import Source
from graphql.utils.build_ast_schema import build_ast_schema
from graphql.utils.schema_printer import print_schema
from graphql.validation import validate


@click.command()
@click.option('--schema', '-s', help='Path to schema file.', required=True)
@click.option('--query', '-q', help='Path to query file.', required=True)
@click.pass_context
def main(ctx, query, schema):
  # Schema
  schema_content = open(schema, 'r').read()
  schema_ast = parse(schema_content)
  schema = build_ast_schema(schema_ast)

  # # Query
  query_content = open(query, 'r').read()
  source = Source(query_content, 'GraphQL request')
  query_ast = parse(source)
  validation_errors = validate(schema, query_ast)
  if validation_errors:
    ctx.fail('\n%s' % '\n'.join([x.message for x in validation_errors]))
  else:
    click.echo("Valid query")

