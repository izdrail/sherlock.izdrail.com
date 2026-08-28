import uuid
import re
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from fastapi_versioning import version
from pydantic import BaseModel

router = APIRouter()

class AnalyzeRequest(BaseModel):
    scenario: str

class AnalyzeResponse(BaseModel):
    risk_level: str  # "High", "Medium", "Low", "Safe"
    score: int  # 0 to 100 risk score
    threat_types: List[str]
    analysis: str
    recommendations: List[str]
    caution_note: str

class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    suggestions: List[str]

class UrlCheckRequest(BaseModel):
    url: str

class UrlCheckResponse(BaseModel):
    url: str
    status: str  # "safe", "suspicious", "malicious"
    risk_score: int
    threats_detected: List[str]
    details: str
    recommendations: List[str]


def analyze_scenario_heuristics(scenario: str) -> AnalyzeResponse:
    text = scenario.lower()
    threats = []
    risk_score = 10

    if any(k in text for k in ["urgent", "wire transfer", "bank details", "gift card", "verify account immediately", "suspicious login"]):
        threats.append("Social Engineering / Urgency Tactic")
        risk_score += 35
    if any(k in text for k in ["click link", "bit.ly", "login.php", "password reset", "verify-your-account"]):
        threats.append("Phishing Link")
        risk_score += 30
    if any(k in text for k in [".exe", "attachment", "zip file", "invoice.pdf.exe", "macro", "download"]):
        threats.append("Malware / Payload Delivery")
        risk_score += 25
    if any(k in text for k in ["irs", "police", "tech support", "microsoft support", "helpdesk"]):
        threats.append("Authority Impersonation")
        risk_score += 20

    risk_score = min(risk_score, 95)

    if risk_score >= 70:
        risk_level = "High"
        summary = "This scenario displays strong indicators of a targeted cyber attack or phishing attempt."
    elif risk_score >= 40:
        risk_level = "Medium"
        summary = "This scenario contains potential security risks. Caution is advised."
    elif risk_score >= 20:
        risk_level = "Low"
        summary = "Low immediate risk detected, but standard cyber hygiene should be maintained."
    else:
        risk_level = "Safe"
        summary = "No obvious social engineering or malicious patterns detected in the provided description."

    recs = [
        "Do not click on unexpected links or open attachments from unknown senders.",
        "Verify the sender's identity through an official secondary channel.",
        "Never share sensitive credentials or payment information over unverified channels."
    ]

    return AnalyzeResponse(
        risk_level=risk_level,
        score=risk_score,
        threat_types=threats if threats else ["General Security Evaluation"],
        analysis=summary,
        recommendations=recs,
        caution_note="AI analysis provides automated guidance and should be combined with organizational security policies."
    )


@router.post("/analyze", response_model=AnalyzeResponse)
@version(1)
async def analyze_threat(request: AnalyzeRequest):
    if not request.scenario.strip():
        raise HTTPException(status_code=400, detail="Scenario description cannot be empty.")
    return analyze_scenario_heuristics(request.scenario)


@router.post("/chat", response_model=ChatResponse)
@version(1)
async def cyber_chat(request: ChatRequest):
    cid = request.conversation_id or str(uuid.uuid4())
    user_msg = request.message.strip().lower()

    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    if "phishing" in user_msg or "scam" in user_msg or "email" in user_msg:
        reply = (
            "Phishing emails often create a false sense of urgency, impersonate trusted brands, "
            "or request confidential information. Check the sender's actual email address domain, "
            "avoid clicking links directly, and report suspicious messages to your security officer."
        )
        suggestions = ["How do I spot fake URLs?", "What should I do if I clicked a link?", "Report phishing"]
    elif "password" in user_msg or "passphrase" in user_msg:
        reply = (
            "Strong passwords should be at least 12-16 characters long, combining uppercase, lowercase, "
            "numbers, and special symbols. Using a unique password for each account along with a trusted password manager is highly recommended."
        )
        suggestions = ["Generate strong password", "What is 2FA?", "Is password manager safe?"]
    elif "2fa" in user_msg or "mfa" in user_msg or "authenticator" in user_msg:
        reply = (
            "Multi-Factor Authentication (MFA) adds a vital layer of security beyond passwords. "
            "Hardware tokens or authenticator apps (like Google or Microsoft Authenticator) are safer than SMS codes."
        )
        suggestions = ["How to enable MFA?", "What if I lose my phone?", "Check URL safety"]
    else:
        reply = (
            f"Regarding your query: standard cybersecurity best practices recommend verifying unexpected communications, "
            "keeping your software updated, using multi-factor authentication, and using complex passwords."
        )
        suggestions = ["Is this email a scam?", "How to report phishing?", "Password security tips"]

    return ChatResponse(
        conversation_id=cid,
        reply=reply,
        suggestions=suggestions
    )


@router.post("/url-check", response_model=UrlCheckResponse)
@version(1)
async def check_url(request: UrlCheckRequest):
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    url_lower = url.lower()
    threats = []
    risk_score = 5

    if re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url_lower):
        threats.append("Raw IP Address used instead of Domain Name")
        risk_score += 40

    if any(susp in url_lower for susp in ["login-", "secure-bank", "paypal-verify", "account-update", "free-gift", "bit.ly", "tinyurl"]):
        threats.append("Typosquatting or Phishing Keyword Pattern")
        risk_score += 35

    if "@" in url_lower or ".exe" in url_lower or ".zip" in url_lower:
        threats.append("Suspicious Payload or Redirect Structure")
        risk_score += 30

    if not url_lower.startswith("https://") and not url_lower.startswith("http://"):
        url_lower = "http://" + url_lower

    if not url_lower.startswith("https://"):
        threats.append("Unencrypted Connection (HTTP)")
        risk_score += 15

    risk_score = min(risk_score, 98)

    if risk_score >= 60:
        status = "malicious"
        details = "High probability of malicious intent or phishing scam."
    elif risk_score >= 25:
        status = "suspicious"
        details = "Proceed with caution. The URL contains patterns often associated with suspicious sites."
    else:
        status = "safe"
        details = "No obvious phishing keywords or suspicious structures detected."

    recs = [
        "Inspect domain names carefully for subtle spelling changes.",
        "Ensure the site uses valid HTTPS before entering any credentials.",
        "Never enter sensitive personal or financial information on unverified sites."
    ]

    return UrlCheckResponse(
        url=url,
        status=status,
        risk_score=risk_score,
        threats_detected=threats if threats else ["None"],
        details=details,
        recommendations=recs
    )
