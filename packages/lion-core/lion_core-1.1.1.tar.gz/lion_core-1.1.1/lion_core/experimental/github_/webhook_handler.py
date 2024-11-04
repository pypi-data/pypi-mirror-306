# # autoos/integrations/github/webhook_handler.py

# import hashlib
# import hmac
# import logging
# import os

# from fastapi import HTTPException, Request

# from .file_operations import FileOperations
# from .flow_operations import FlowOperations
# from .issue_operations import IssueOperations
# from .pr_operations import PROperations
# from .repo_operations import RepoOperations

# logger = logging.getLogger(__name__)


# class WebhookHandler:

#     @staticmethod
#     async def handle_webhook(request: Request):
#         # Verify GitHub webhook signature
#         signature = request.headers.get("X-Hub-Signature-256")
#         if not signature:
#             logger.warning("No signature provided in the webhook request.")
#             raise HTTPException(
#                 status_code=400, detail="No signature provided"
#             )

#         body = await request.body()
#         secret = os.getenv("GITHUB_WEBHOOK_SECRET")
#         if not secret:
#             logger.error(
#                 "GITHUB_WEBHOOK_SECRET is not set in the environment variables."
#             )
#             raise HTTPException(
#                 status_code=500, detail="Server configuration error"
#             )
#         secret = secret.encode()

#         expected_signature = (
#             "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()
#         )

#         if not hmac.compare_digest(signature, expected_signature):
#             logger.warning("Invalid webhook signature.")
#             raise HTTPException(status_code=400, detail="Invalid signature")

#         # Process the webhook payload
#         payload = await request.json()
#         event_type = request.headers.get("X-GitHub-Event")
#         action = payload.get("action", "")

#         repo_name = payload.get("repository", {}).get("full_name", "Unknown")

#         # Handle different event types
#         if event_type == "issues":
#             logger.info(f"Received an issues event: {action}")
#             await WebhookHandler.handle_issue_event(repo_name, payload, action)
#         elif event_type == "pull_request":
#             logger.info(f"Received a pull request event: {action}")
#             await WebhookHandler.handle_pull_request_event(
#                 repo_name, payload, action
#             )
#         elif event_type == "push":
#             logger.info("Received a push event.")
#             await WebhookHandler.handle_push_event(repo_name, payload)
#         else:
#             logger.info(f"Received unhandled event type: {event_type}")
#             # Handle other event types if necessary

#         return {"message": "Webhook processed successfully"}

#     @staticmethod
#     async def handle_issue_event(repo_name: str, payload: dict, action: str):
#         issue_number = payload["issue"]["number"]
#         if action == "opened":
#             # Auto-reply to new issues
#             comment = "Thank you for opening this issue. We will look into it shortly."
#             IssueOperations.create_issue_comment(
#                 repo_name, issue_number, comment
#             )
#             logger.info(
#                 f"Auto-replied to issue #{issue_number} in {repo_name}"
#             )
#             # Additional processing can be done here (e.g., labeling, assigning)

#     @staticmethod
#     async def handle_pull_request_event(
#         repo_name: str, payload: dict, action: str
#     ):
#         pr_number = payload["pull_request"]["number"]
#         if action == "opened":
#             # Perform automated code review
#             pr = PROperations.get_pull_request(repo_name, pr_number)
#             # Example: Add a general comment
#             comment = "Thank you for the pull request! We will review it soon."
#             pr.create_issue_comment(comment)
#             logger.info(f"Added a comment to PR #{pr_number} in {repo_name}")
#             # Additional code analysis can be performed here

#     @staticmethod
#     async def handle_push_event(repo_name: str, payload: dict):
#         # Implement push event handling logic here
#         # Example: Trigger automated tests
#         ref = payload["ref"]
#         if ref == "refs/heads/main":
#             logger.info(
#                 f"Push to main branch in {repo_name}. Triggering CI/CD pipeline."
#             )
#             # Trigger CI/CD pipeline
#             pass
#         else:
#             logger.info(f"Push to {ref} in {repo_name}.")
#             # Handle other branches if necessary

#     @staticmethod
#     async def handle_issue_event(repo_name: str, payload: dict, action: str):
#         issue_number = payload["issue"]["number"]
#         if action == "opened":
#             # Trigger the issue_to_fix_flow
#             logger.info(
#                 f"Starting issue_to_fix_flow for issue #{issue_number} in {repo_name}"
#             )
#             FlowOperations.issue_to_fix_flow(repo_name, issue_number)
#         # Handle other actions if needed

#     @staticmethod
#     async def handle_pull_request_event(
#         repo_name: str, payload: dict, action: str
#     ):
#         pr_number = payload["pull_request"]["number"]
#         if action == "opened":
#             # Trigger the automated_code_review_flow
#             logger.info(
#                 f"Starting automated_code_review_flow for PR #{pr_number} in {repo_name}"
#             )
#             FlowOperations.automated_code_review_flow(repo_name, pr_number)
#         # Handle other actions if needed
