"""
TERASS Adviser API Server
REST API for integrating TERASS business logic with ChatGPT and other external systems.

This API exposes:
- Reward calculation endpoints
- Agent class determination endpoints  
- Opinion/feedback submission endpoints

Authentication: Bearer token via X-API-Token header
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from typing import List, Dict, Any

from src.engine.reward_calculator import calc_portfolio_reward, calc_reward_for_deal, Deal
from src.engine.agent_class import determine_class, AgentRecord

app = Flask(__name__)
CORS(app)

# Authentication token from environment - REQUIRED
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    print("WARNING: API_TOKEN environment variable not set. Using default token for development only.")
    print("For production, always set a secure API_TOKEN environment variable.")
    API_TOKEN = "terass-api-token-2025"  # Development default only
FEEDBACK_FILE = "feedback_data.json"


def require_auth():
    """Check for valid API token in request headers"""
    token = request.headers.get("X-API-Token")
    if not token or token != API_TOKEN:
        return jsonify({"error": "Unauthorized", "message": "Valid X-API-Token header required"}), 401
    return None


@app.route("/", methods=["GET"])
def index():
    """API information endpoint"""
    return jsonify({
        "name": "TERASS Adviser API",
        "version": "1.0.0",
        "description": "REST API for TERASS business operations",
        "endpoints": {
            "reward_calculation": "/api/v1/reward/calculate",
            "agent_class": "/api/v1/agent/class",
            "feedback": "/api/v1/feedback",
            "health": "/api/v1/health"
        }
    })


@app.route("/api/v1/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/v1/reward/calculate", methods=["POST"])
def calculate_reward():
    """
    Calculate reward for one or more deals.
    
    Request body:
    {
        "deals": [
            {
                "tax_excluded_fee": 5000000,
                "source": "self",
                "date": "2025-04-01"
            }
        ]
    }
    
    Response:
    {
        "total_reward": 3750000,
        "details": [...]
    }
    """
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    if not data or "deals" not in data:
        return jsonify({"error": "Bad Request", "message": "Missing 'deals' in request body"}), 400
    
    try:
        deals = []
        for deal_data in data["deals"]:
            deal = Deal(
                tax_excluded_fee=float(deal_data.get("tax_excluded_fee", 0)),
                source=deal_data.get("source", "self"),
                date=deal_data.get("date", datetime.now().strftime("%Y-%m-%d"))
            )
            deals.append(deal)
        
        result = calc_portfolio_reward(deals)
        
        # Convert Deal objects to dict for JSON serialization
        serializable_result = {
            "total_reward": result["total_reward"],
            "details": [
                {
                    "deal": {
                        "tax_excluded_fee": detail["deal"].tax_excluded_fee,
                        "source": detail["deal"].source,
                        "date": detail["deal"].date
                    },
                    "reward_amount": detail["reward_amount"],
                    "rate_applied": detail["rate_applied"],
                    "bonus_activated": detail["bonus_activated"],
                    "year_to_date_after": detail["year_to_date_after"]
                }
                for detail in result["details"]
            ]
        }
        
        return jsonify(serializable_result)
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@app.route("/api/v1/agent/class", methods=["POST"])
def determine_agent_class():
    """
    Determine agent class based on performance metrics.
    
    Request body:
    {
        "region": "capital",
        "period_sales": 4500000,
        "cumulative_cases": 3
    }
    
    Response:
    {
        "class": "Unranked",
        "needed_sales": 500000,
        "needed_cases": 2
    }
    """
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message": "Missing request body"}), 400
    
    try:
        record = AgentRecord(
            region=data.get("region", "capital"),
            period_sales=float(data.get("period_sales", 0)),
            cumulative_cases=int(data.get("cumulative_cases", 0))
        )
        
        result = determine_class(record)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@app.route("/api/v1/feedback", methods=["POST"])
def submit_feedback():
    """
    Submit feedback or opinion from ChatGPT or other users.
    
    Request body:
    {
        "user_id": "agent123",
        "category": "feature_request",
        "message": "Please add more loan options",
        "context": {...}
    }
    
    Response:
    {
        "success": true,
        "feedback_id": "fb_123456"
    }
    """
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Bad Request", "message": "Missing 'message' in request body"}), 400
    
    try:
        # Create feedback entry
        feedback_entry = {
            "id": f"fb_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "user_id": data.get("user_id", "anonymous"),
            "category": data.get("category", "general"),
            "message": data.get("message"),
            "context": data.get("context", {}),
            "status": "pending"
        }
        
        # Load existing feedback
        feedback_list = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                feedback_list = json.load(f)
        
        # Append new feedback
        feedback_list.append(feedback_entry)
        
        # Save feedback
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(feedback_list, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "feedback_id": feedback_entry["id"],
            "message": "Feedback submitted successfully"
        })
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@app.route("/api/v1/feedback", methods=["GET"])
def list_feedback():
    """
    List all submitted feedback.
    
    Query params:
    - status: filter by status (pending, reviewed, resolved)
    - limit: maximum number of results (default: 100)
    
    Response:
    {
        "feedback": [...],
        "count": 10
    }
    """
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        status_filter = request.args.get("status")
        limit = int(request.args.get("limit", 100))
        
        feedback_list = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                feedback_list = json.load(f)
        
        # Apply filters
        if status_filter:
            feedback_list = [f for f in feedback_list if f.get("status") == status_filter]
        
        # Apply limit
        feedback_list = feedback_list[-limit:]
        
        return jsonify({
            "feedback": feedback_list,
            "count": len(feedback_list)
        })
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
