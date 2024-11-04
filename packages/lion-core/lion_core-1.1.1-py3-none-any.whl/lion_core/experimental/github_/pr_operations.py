# # autoos/integrations/github/pr_operations.py

# from .github_client import github_client, logger


# class PROperations:
#     @staticmethod
#     def create_pull_request(
#         repo_name: str, title: str, body: str, head: str, base: str
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             pr = repo.create_pull(title=title, body=body, head=head, base=base)
#             logger.info(f"Created pull request: {pr.html_url}")
#             return pr
#         except Exception as e:
#             logger.error(
#                 f"Error creating pull request in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def get_pull_request(repo_name: str, pr_number: int):
#         repo = github_client.get_repo(repo_name)
#         try:
#             pr = repo.get_pull(pr_number)
#             logger.info(f"Fetched pull request #{pr_number} from {repo_name}")
#             return pr
#         except Exception as e:
#             logger.error(
#                 f"Error fetching pull request #{pr_number} from {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def list_pull_requests(repo_name: str, state: str = "open"):
#         repo = github_client.get_repo(repo_name)
#         try:
#             pulls = repo.get_pulls(state=state)
#             pr_list = [pr for pr in pulls]
#             logger.info(f"Listed {state} pull requests in {repo_name}")
#             return pr_list
#         except Exception as e:
#             logger.error(
#                 f"Error listing {state} pull requests in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def merge_pull_request(
#         repo_name: str,
#         pr_number: int,
#         commit_message: str = None,
#         merge_method: str = "merge",
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             pr = repo.get_pull(pr_number)
#             merge_result = pr.merge(
#                 commit_message=commit_message, merge_method=merge_method
#             )
#             if merge_result.merged:
#                 logger.info(
#                     f"Successfully merged pull request #{pr_number} in {repo_name}"
#                 )
#                 return merge_result
#             else:
#                 logger.warning(
#                     f"Failed to merge pull request #{pr_number} in {repo_name}: {merge_result.message}"
#                 )
#                 raise Exception(merge_result.message)
#         except Exception as e:
#             logger.error(
#                 f"Error merging pull request #{pr_number} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def close_pull_request(repo_name: str, pr_number: int):
#         repo = github_client.get_repo(repo_name)
#         try:
#             pr = repo.get_pull(pr_number)
#             pr.edit(state="closed")
#             logger.info(f"Closed pull request #{pr_number} in {repo_name}")
#             return pr
#         except Exception as e:
#             logger.error(
#                 f"Error closing pull request #{pr_number} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def create_review_comment(
#         repo_name: str,
#         pr_number: int,
#         body: str,
#         commit_id: str,
#         path: str,
#         position: int,
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             pr = repo.get_pull(pr_number)
#             comment = pr.create_review_comment(
#                 body=body, commit_id=commit_id, path=path, position=position
#             )
#             logger.info(
#                 f"Added review comment to PR #{pr_number} in {repo_name}"
#             )
#             return comment
#         except Exception as e:
#             logger.error(
#                 f"Error adding review comment to PR #{pr_number} in {repo_name}: {str(e)}"
#             )
#             raise

#     # Add more PR-related operations as needed
