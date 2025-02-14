# **Mitigating Rogue OIDC Identity Provider Attacks in AWS**

## **Introduction**
AWS OpenID Connect (OIDC) federation allows organizations to delegate authentication to external identity providers. This helps eliminate long-lived access keys, improving security. However, **misconfigurations in IAM trust policies** and AWS's **implicit trust in any correctly configured OIDC provider** introduce critical security risks. 

### **The Attack: Exploiting Rogue OIDC Providers**

Attackers can exploit misconfigured OIDC integrations in AWS by:

1. **Creating a Malicious OIDC Provider** – Hosting a fake OIDC provider with a valid HTTPS certificate and registering it in AWS.
2. **Exploiting IAM Trust Policies** – If an IAM role allows assumptions from any OIDC provider without strict conditions (`aud`, `sub`), attackers can forge JWTs and assume the role.
3. **Evasion Techniques** – Mimicking legitimate OIDC providers (e.g., Terraform Cloud, GitHub Actions) and generating unique session names to bypass detection.

---

## **Root Cause Analysis**

### **1. AWS Implicitly Trusts Any Registered OIDC Provider**
AWS does not verify whether an OIDC provider is legitimate; it only checks that it has **valid HTTPS certificates**. This means attackers can create and register rogue OIDC providers without AWS detecting malicious intent.

### **2. Overly Permissive IAM Role Trust Configurations**
Organizations often misconfigure IAM trust relationships by:
- **Missing `aud` (audience) and `sub` (subject) conditions**, allowing any token from the registered provider.
- **Failing to limit the trust policy to specific known clients**.
- **Not monitoring modifications to trust relationships**, enabling attackers to inject their rogue provider.

### **3. Weak Monitoring and Detection**
Many organizations **do not actively monitor OIDC provider additions or role assumptions**, making it easy for attackers to operate undetected.

---

## **Prevention Strategies**

To mitigate this attack, organizations should follow strict **least privilege principles**, enforce **tight IAM trust policies**, and implement **continuous monitoring**.

### **1. Restrict IAM Permissions for OIDC Provider Management**

Limit which IAM users can create or modify OIDC providers and trust relationships.

#### **Use an AWS IAM Policy to Block Unauthorized OIDC Provider Creation**
```json
{
  "Effect": "Deny",
  "Action": [
    "iam:CreateOpenIDConnectProvider",
    "iam:UpdateOpenIDConnectProviderThumbprint",
    "iam:DeleteOpenIDConnectProvider"
  ],
  "Resource": "*"
}
```
Apply this policy to all users except those explicitly authorized.

---

### **2. Enforce Strict IAM Trust Conditions for OIDC Roles**

To prevent unauthorized role assumptions, trust relationships should **require explicit `aud` (audience) and `sub` (subject) conditions**.

#### **Example Secure IAM Trust Policy for OIDC Roles**
```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/valid-provider.com"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "valid-provider.com:aud": "expected-client-id",
      "valid-provider.com:sub": "trusted-user"
    }
  }
}
```

✅ **Key Fixes:**
- Ensures only **specific workloads** (`aud`) and **trusted identities** (`sub`) can assume the role.
- Prevents unauthorized clients from using the same OIDC provider.

---

### **3. Implement Monitoring and Detection Controls**

Enable AWS security tools to **detect suspicious role assumptions and trust modifications**.

#### **Monitor OIDC Provider Creation and Trust Changes Using CloudTrail**

Set up AWS **CloudWatch Alarms** for IAM OIDC-related events:
```json
{
  "source": ["aws.iam"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventName": [
      "CreateOpenIDConnectProvider", 
      "UpdateAssumeRolePolicy", 
      "AssumeRoleWithWebIdentity"
    ]
  }
}
```

✅ **What this does:**
- Alerts on **new OIDC providers being created**.
- Detects **modifications to IAM role trust relationships**.
- Identifies **unusual role assumption attempts**.

#### **Review OIDC Providers Periodically**
Use the following AWS CLI commands to **list, review, and remove** unused OIDC providers:
```sh
aws iam list-open-id-connect-providers
aws iam get-open-id-connect-provider --open-id-connect-provider-arn <OIDC_PROVIDER_ARN>
aws iam delete-open-id-connect-provider --open-id-connect-provider-arn <OIDC_PROVIDER_ARN>
```

---

### **4. Strengthen OIDC Integrations**

For cloud-native platforms like **GitHub Actions, Terraform Cloud, and GitLab**, follow **vendor security best practices**:
- **GitHub Actions**: Restrict repository access and limit OIDC tokens to specific workflows.
- **Terraform Cloud**: Ensure `aud` claims are validated in AWS.
- **GitLab**: Use fine-grained IAM policies for OIDC authentication.

---

### **5. Use AWS Security Tools for Anomaly Detection**

#### **Enable GuardDuty to Detect Anomalies in OIDC Role Assumptions**
AWS GuardDuty can detect unusual behavior such as:
- **Multiple role assumptions from different locations.**
- **Anomalous session activity (e.g., frequent session changes).**
- **Unrecognized OIDC providers.**

#### **Use AWS Config to Ensure Compliance**
AWS Config can track and alert on:
- **Non-compliant IAM roles missing `aud` or `sub` conditions.**
- **Changes in IAM trust relationships.**

---

### **6. Educate Teams and Regularly Test Defenses**
- Conduct **red-team exercises** to test role assumption risks.
- Train security and DevOps teams on **proper OIDC configurations**.
- Promote **use of temporary credentials** over long-lived access keys.
- **Periodically rotate OIDC keys** if self-hosting an identity provider.

---

## **Conclusion**
The **Rogue OIDC attack** leverages AWS's **implicit trust in identity providers** and **weak IAM trust configurations** to gain persistent access to AWS resources. 

To prevent this:
✅ **Restrict who can create or modify OIDC providers**.  
✅ **Implement strict `aud` and `sub` conditions in IAM trust policies**.  
✅ **Continuously monitor IAM role assumptions and trust modifications**.  
✅ **Use AWS GuardDuty, Config, and CloudTrail for anomaly detection**.  
✅ **Regularly audit OIDC providers and enforce security best practices**.  

By applying these strategies, organizations can **securely leverage OIDC authentication** without exposing themselves to **identity-based AWS attacks**.

---

## **Further Reading & Tools**
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [RogueOIDC GitHub Repo](https://github.com/OffensAI/RogueOIDC)  
- [AWS GuardDuty Detection for IAM](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html)  
