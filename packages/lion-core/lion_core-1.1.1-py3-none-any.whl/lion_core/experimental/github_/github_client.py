# # autoos/integrations/github/github_client.py

# import logging
# import os

# from dotenv import load_dotenv
# from github import Github

# load_dotenv()

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# class GitHubClient:
#     def __init__(self):
#         try:
#             token = os.getenv("GITHUB_ACCESS_TOKEN")
#             if not token:
#                 raise ValueError(
#                     "GITHUB_ACCESS_TOKEN is not set in the environment variables."
#                 )
#             self.github = Github(token)
#             self.user = self.github.get_user()
#             logger.info(
#                 f"Initialized GitHub client for user: {self.user.login}"
#             )
#         except Exception as e:
#             logger.error(f"Failed to initialize GitHub client: {str(e)}")
#             raise

#     def get_repo(self, repo_name: str):
#         try:
#             return self.user.get_repo(repo_name)
#         except Exception as e:
#             logger.error(f"Error accessing repository {repo_name}: {str(e)}")
#             raise
