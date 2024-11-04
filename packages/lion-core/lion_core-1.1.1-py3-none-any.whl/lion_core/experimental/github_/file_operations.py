# # Filepath: /autoos/integrations/github/file_operations.py

# from .github_client import github_client, logger
# from .utils import decode_content


# class FileOperations:
#     @staticmethod
#     def create_file(
#         repo_name: str, file_path: str, content: str, commit_message: str
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             repo.create_file(file_path, commit_message, content)
#             logger.info(f"Created file {file_path} in {repo_name}")
#         except Exception as e:
#             logger.error(
#                 f"Error creating file {file_path} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def update_file(
#         repo_name: str,
#         file_path: str,
#         content: str,
#         commit_message: str,
#         branch: str = "main",
#     ):
#         repo = github_client.get_repo(repo_name)
#         try:
#             contents = repo.get_contents(file_path, ref=branch)
#             repo.update_file(
#                 contents.path,
#                 commit_message,
#                 content,
#                 contents.sha,
#                 branch=branch,
#             )
#             logger.info(
#                 f"Updated file {file_path} in {repo_name} on branch {branch}"
#             )
#         except Exception as e:
#             logger.error(
#                 f"Error updating file {file_path} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def read_file(repo_name: str, file_path: str):
#         repo = github_client.get_repo(repo_name)
#         try:
#             contents = repo.get_contents(file_path)
#             content = decode_content(contents.content)
#             logger.info(f"Read file {file_path} in {repo_name}")
#             return content
#         except Exception as e:
#             logger.error(
#                 f"Error reading file {file_path} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def delete_file(repo_name: str, file_path: str, commit_message: str):
#         repo = github_client.get_repo(repo_name)
#         try:
#             contents = repo.get_contents(file_path)
#             repo.delete_file(contents.path, commit_message, contents.sha)
#             logger.info(f"Deleted file {file_path} in {repo_name}")
#         except Exception as e:
#             logger.error(
#                 f"Error deleting file {file_path} in {repo_name}: {str(e)}"
#             )
#             raise

#     @staticmethod
#     def get_file_content(repo_name: str, file_path: str, ref: str = None):
#         repo = github_client.get_repo(repo_name)
#         try:
#             contents = repo.get_contents(file_path, ref=ref)
#             content = decode_content(contents.content)
#             logger.info(
#                 f"Retrieved content of file {file_path} in {repo_name}"
#                 + (f" at {ref}" if ref else "")
#             )
#             return content
#         except Exception as e:
#             logger.error(
#                 f"Error getting content of file {file_path} in {repo_name}: {str(e)}"
#             )
#             raise
