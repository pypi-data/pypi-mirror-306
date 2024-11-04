# # autoos/integrations/github/issue_operations.py

# from .github_client import github_client, logger


# class IssueOperations:
#     @staticmethod
#     def create_issue(repo_name: str, title: str, body: str):
#         repo = github_client.get_repo(repo_name)
#         try:
#             issue = repo.create_issue(title=title, body=body)
#             logger.info(f"Created issue: {issue.html_url}")
#             return issue
#         except Exception as e:
#             logger.error(f"Error creating issue in {repo_name}: {str(e)}")
#             raise

#     @staticmethod
#     def create_issue_comment(repo_name: str, issue_number: int, comment: str):
#         repo = github_client.get_repo(repo_name)
#         try:
#             issue = repo.get_issue(number=issue_number)
#             issue.create_comment(body=comment)
#             logger.info(f"Commented on issue #{issue_number} in {repo_name}")
#             return issue
#         except Exception as e:
#             logger.error(
#                 f"Error commenting on issue #{issue_number} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def get_issue(repo_name: str, issue_number: int):
#         repo = github_client.get_repo(repo_name)
#         try:
#             issue = repo.get_issue(number=issue_number)
#             logger.info(f"Fetched issue #{issue_number} from {repo_name}")
#             return issue
#         except Exception as e:
#             logger.error(
#                 f"Error fetching issue #{issue_number} from {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def close_issue(repo_name: str, issue_number: int):
#         repo = github_client.get_repo(repo_name)
#         try:
#             issue = repo.get_issue(number=issue_number)
#             issue.edit(state="closed")
#             logger.info(f"Closed issue #{issue_number} in {repo_name}")
#             return issue
#         except Exception as e:
#             logger.error(
#                 f"Error closing issue #{issue_number} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def reopen_issue(repo_name: str, issue_number: int):
#         repo = github_client.get_repo(repo_name)
#         try:
#             issue = repo.get_issue(number=issue_number)
#             issue.edit(state="open")
#             logger.info(f"Reopened issue #{issue_number} in {repo_name}")
#             return issue
#         except Exception as e:
#             logger.error(
#                 f"Error reopening issue #{issue_number} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def list_issues(repo_name: str, state: str = "open"):
#         repo = github_client.get_repo(repo_name)
#         try:
#             issues = repo.get_issues(state=state)
#             issue_list = [issue for issue in issues]
#             logger.info(f"Listed {state} issues in {repo_name}")
#             return issue_list
#         except Exception as e:
#             logger.error(
#                 f"Error listing {state} issues in {repo_name}: {str(e)}"
#             )
#             raise

#     # Add more issue-related operations as needed
