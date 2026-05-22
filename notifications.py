
#Method 2 - borrowed from proj_awf_sales
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText

# Set up logging for your module
logger = logging.getLogger(__name__)

def send_error_email(error_message: str, table_name: str):
    """Sends an automated email notification when the database pipeline fails using your proven working settings."""
    
    # --- EMAIL CONFIGURATION ---
    sender_email = "alan.yao@hunterdouglas.com.au"
    receiver_email = "alan.yao@hunterdouglas.com.au"
    
    # IMPORTANT: Replace "xxxx" with the actual working password/token from your other project
    password = "hd9999" 
    
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Build the message string exactly like your working model
    email_body = (
        f"The SQL Load script failed with the following error - @{timestamp_str} :\n\n"
        f"Target Table: JDE_DB_ALAN.{table_name}\n"
        f"Error Details:\n{error_message}"
    )
    
    msg = MIMEText(email_body)
    msg["Subject"] = f"❌ ALERT: SQL Load Failure ({table_name})"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            
        logger.info(f"Alert email successfully dispatched to {receiver_email}")
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")





'''       
# Below code should be working but need set up Microsoft account properly or need IT approval
# Way 1 - require new set up in your microsoft account or ask IT permission 
# Option 1: Generate a Microsoft App Password (Easiest & Quickest)
# If your corporate account allows it, you can create a unique password specifically for this Python script that bypasses MFA blocks:
# Go to your Microsoft My Account security page (microsoft.com). Click Add sign-in method and select App password.
# Name it something like Python Pipeline and click Next. Microsoft will give you a 16-character password string (e.g., abcd efgh ijkl mnop).
# Copy that string and paste it into your notifications.py file as your sender_password.

# Option 2: Use Your Company's Internal SMTP Relay (Most Professional)
# Large organizations usually have an internal email server rule called an SMTP Relay that allows trusted scripts to send emails automatically without requiring any passwords or MFA tokens.
# Email or chat your company's IT Support / Network Administration team.
# Ask them this exact question:
#"Hi IT Team, I am setting up an automated Python database pipeline script on a local server. What is our internal SMTP Relay server address and Port that I can use to send out automated failure alerts without authentication?"
# Once they give you the address (it usually looks like ://yourcompany.com or an IP address like 10.x.x.x), you put that address into your script, change the port to what they tell you (usually 25), and remove/delete the login credentials completely:


# How your code looks if IT gives you an internal relay:
smtp_server = "://yourcompany.com" 
smtp_port = 25 # or what IT specifies
sender_email = "pipeline-alerts@yourcompany.com"
receiver_email = "your-email@yourcompany.com"

# Remove or comment out server.login() since relays don't use passwords:
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls() 
    # server.login(sender_email, sender_password) <-- Deleted/Commented out!
    server.send_message(msg)

    
'''





# Below is original Method 1 

# import smtplib
# import logging
# from datetime import datetime
# from email.mime.text import MIMEText

# # Set up logging for your module
# logger = logging.getLogger(__name__)

# def send_error_email(error_message: str, table_name: str):
#     """Sends an automated email notification when the database pipeline fails using your proven working settings."""
    
#     # --- EMAIL CONFIGURATION ---
#     sender_email = "alan.yao@hunterdouglas.com.au"
#     receiver_email = "alan.yao@hunterdouglas.com.au"
    
#     # IMPORTANT: Replace "xxxx" with the actual working password/token from your other project
#     password = "xxxx" 
    
#     smtp_server = "://office365.com"
#     smtp_port = 587
    
#     now = datetime.now()
#     timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
#     # Build the message string exactly like your working model
#     email_body = (
#         f"The SQL Load script failed with the following error - @{timestamp_str} :\n\n"
#         f"Target Table: JDE_DB_ALAN.{table_name}\n"
#         f"Error Details:\n{error_message}"
#     )
    
#     msg = MIMEText(email_body)
#     msg["Subject"] = f"❌ ALERT: SQL Load Failure ({table_name})"
#     msg["From"] = sender_email
#     msg["To"] = receiver_email
    
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  # Secure the connection
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
            
#         logger.info(f"Alert email successfully dispatched to {receiver_email}")
        
#     except Exception as e:
#         logger.error(f"Failed to send email notification: {e}")

        

