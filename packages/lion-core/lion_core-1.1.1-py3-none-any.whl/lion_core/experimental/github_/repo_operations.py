# # autoos/integrations/github/repo_operations.py

# from .github_client import github_client, logger


# class RepoOperations:
#     @staticmethod
#     def create_repo(
#         repo_name: str, description: str = "", private: bool = False
#     ):
#         try:
#             repo = github_client.user.create_repo(
#                 name=repo_name, description=description, private=private
#             )
#             logger.info(f"Created new repository: {repo.full_name}")
#             return repo
#         except Exception as e:
#             logger.error(f"Error creating repository {repo_name}: {str(e)}")
#             raise

#     @staticmethod
#     def get_repo_contents(repo_name: str, path: str = ""):
#         repo = github_client.get_repo(repo_name)
#         try:
#             contents = repo.get_contents(path)
#             file_list = []
#             if isinstance(contents, list):
#                 for content_file in contents:
#                     file_list.append(
#                         {"type": content_file.type, "path": content_file.path}
#                     )
#             else:
#                 file_list.append(
#                     {"type": contents.type, "path": contents.path}
#                 )
#             logger.info(f"Fetched contents of {repo_name}/{path}")
#             return file_list
#         except Exception as e:
#             logger.error(
#                 f"Error getting contents of {repo_name}/{path}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def delete_repo(repo_name: str):
#         try:
#             repo = github_client.get_repo(
#                 f"{github_client.user.login}/{repo_name}"
#             )
#             repo.delete()
#             logger.info(f"Deleted repository: {repo_name}")
#         except Exception as e:
#             logger.error(f"Error deleting repository {repo_name}: {str(e)}")
#             raise

#     @staticmethod
#     def create_branch(
#         repo_name: str, new_branch: str, source_branch: str = "main"
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             source_ref = repo.get_git_ref(f"heads/{source_branch}")
#             repo.create_git_ref(
#                 ref=f"refs/heads/{new_branch}", sha=source_ref.object.sha
#             )
#             logger.info(
#                 f"Created new branch '{new_branch}' from '{source_branch}' in {repo_name}"
#             )
#         except Exception as e:
#             logger.error(
#                 f"Error creating branch '{new_branch}' in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def delete_branch(repo_name: str, branch_name: str):
#         repo = github_client.get_repo(repo_name)
#         try:
#             ref = repo.get_git_ref(f"heads/{branch_name}")
#             ref.delete()
#             logger.info(f"Deleted branch '{branch_name}' in {repo_name}")
#         except Exception as e:
#             logger.error(
#                 f"Error deleting branch '{branch_name}' in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def get_commit_history(
#         repo_name: str, branch_name: str = "main", limit: int = 100
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             commits = repo.get_commits(sha=branch_name)[:limit]
#             commit_list = [
#                 {"sha": commit.sha, "message": commit.commit.message}
#                 for commit in commits
#             ]
#             logger.info(
#                 f"Fetched {len(commit_list)} commits from branch '{branch_name}' in {repo_name}"
#             )
#             return commit_list
#         except Exception as e:
#             logger.error(
#                 f"Error fetching commits from {repo_name}/{branch_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def compare_branches(repo_name: str, base: str, head: str):
#         repo = github_client.get_repo(repo_name)
#         try:
#             comparison = repo.compare(base, head)
#             logger.info(
#                 f"Compared branches '{base}' and '{head}' in {repo_name}"
#             )
#             return comparison
#         except Exception as e:
#             logger.error(
#                 f"Error comparing branches '{base}' and '{head}' in {repo_name}: {str(e)}"
#             )
#             raise

#     # Add more repository-related operations as needed
