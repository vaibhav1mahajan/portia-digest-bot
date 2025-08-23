"""Email sender using Portia SDK and Gmail tool."""

from typing import Optional
from portia import (
    Config,
    DefaultToolRegistry,
    Portia,
    StorageClass,
)
from portia.cli import CLIExecutionHooks


class PortiaEmailSender:
    """Send emails using Portia's Gmail tool."""
    
    def __init__(self):
        """Initialize Portia SDK for email sending."""
        # Use the same configuration as a.py
        my_config = Config.from_default(storage_class=StorageClass.CLOUD)
        self.portia = Portia(
            config=my_config,
            tools=DefaultToolRegistry(my_config),
            execution_hooks=CLIExecutionHooks(),
        )
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        timeout: int = 120
    ) -> bool:
        """Send email using Portia's Gmail tool."""
        
        # Create the email sending prompt (similar to a.py)
        email_prompt = f"send email to {to_email} with subject '{subject}' and body '{body}'"
        
        try:
            print(f"📤 Sending email to {to_email} via Portia...")
            
            # Use Portia to send the email (same as a.py)
            plan_run = self.portia.run(email_prompt)
            
            # Get the output (same as a.py)
            if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
                output = plan_run.outputs.final_output
            elif hasattr(plan_run, 'final_output'):
                output = plan_run.final_output
            elif hasattr(plan_run, 'output'):
                output = plan_run.output
            else:
                output = "No output"
            
            print(f"📧 Result: {output}")
            
            # Check for success indicators
            success_indicators = [
                "email sent", "sent successfully", "success", "sent", 
                "email delivered", "gmail", "sent via", "delivered"
            ]
            
            output_str = str(output).lower()
            is_success = any(indicator in output_str for indicator in success_indicators)
            
            if is_success:
                print(f"✅ Email sent successfully to {to_email}")
                return True
            else:
                print(f"⚠️  Email sending result unclear")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def close(self):
        """Clean up resources."""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
