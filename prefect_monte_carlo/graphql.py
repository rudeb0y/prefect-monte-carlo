"""Module for GraphQL queries and mutations."""

from typing import Any, Dict, Optional

from prefect import task

from prefect_monte_carlo.credentials import MonteCarloCredentials


@task
async def execute_graphql_operation(
    montecarlo_credentials: MonteCarloCredentials,
    operation: str,
    variables: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Executes a GraphQL operation via the Monte Carlo GraphQL API.

    Args:
        montecarlo_credentials: credentials to authenticate with the
            Monte Carlo GraphQL API.
        operation: the GraphQL operation to execute - it can be a valid GraphQL
            query or mutation.
        variables: the variables to pass to the GraphQL operation.

    Returns:
        The results of the GraphQL operation.

    Example:
        Executes a simple GraphQL query against the Monte Carlo GraphQL API.
        ```python
        from prefect import flow
        from prefect_monte_carlo import execute_graphql_operation
        from prefect_monte_carlo.credentials import MonteCarloCredentials

        @flow
        def example_execute_query():
            montecarlo_credentials = MonteCarloCredentials.load(
                "my-montecarlo-credentials"
            )
            result = execute_graphql_operation(
                montecarlo_credentials=montecarlo_credentials,
                operation="query getUser { getUser { email firstName lastName }}",
            )

        example_execute_query()
        ```

        Executes a GraphQL query with variables.
        ```python
        from prefect import flow

        from prefect_monte_carlo.credentials import MonteCarloCredentials
        from prefect_monte_carlo.graphql import execute_graphql_operation

        mc_creds = MonteCarloCredentials.load("monte-carlo-credentials")

        query = '''
            query getTables($first: Int){
                getTables(first: $first) {
                    edges {
                        node {
                            fullTableId
                        }
                    }
                }
            }
        '''

        @flow
        def test_mc():

            result = execute_graphql_operation(
                montecarlo_credentials=mc_creds,
                operation=query,
                variables={"first":10}
            )

        if __name__ == "__main__":
            test_mc()
        ```
    """
    client = montecarlo_credentials.get_client()
    return client(operation, variables=variables)
