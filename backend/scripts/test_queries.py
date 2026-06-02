#!/usr/bin/env python3
"""Test all sample queries against the running backend and report results."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx

BASE_URL = "http://localhost:8000"

QUERIES = {
    "TP SEN Support": [
        "How do I apply for SEN support at TP?",
        "What disabilities does TP's SEN support cover?",
        "Where is the SEN support office located in TP?",
        "What is the MOE SEN fund and how do I apply?",
        "Can TP students with learning disabilities get exam accommodations?",
        "Who do I contact for SEN support at Temasek Polytechnic?",
        "What assistive technology does TP provide for disabled students?",
        "I have ADHD — what support can I get at TP?",
        "Does TP have counselling services for students with disabilities?",
        "What is a caring campus at TP?",
    ],
    "Disability Transport": [
        "What transport subsidies are available for persons with disabilities in Singapore?",
        "How do I apply for the taxi subsidy scheme?",
        "What is the PWD concession card and how do I get one?",
        "Is there a bus fare discount for wheelchair users?",
        "What is the Enabling Transport Subsidy?",
        "How much does the taxi subsidy cover for disabled persons?",
        "Can I get a car park label as a person with a disability?",
        "What documents do I need to apply for disability transport schemes?",
        "Is the taxi subsidy means-tested?",
        "What transport help is available for a child with autism?",
    ],
    "Care Services": [
        "What day activity centres are available for adults with disabilities?",
        "What is a sheltered workshop in Singapore?",
        "How do I find a disability home for my adult child?",
        "What is ESLP and who is it for?",
        "Are there hostels for adults with disabilities in Singapore?",
        "What is the Assisted Deputyship Application Programme?",
        "What care options exist for a person with severe intellectual disability?",
        "How do I get information and referral services for disability care?",
        "What is the ELP and HSP programme?",
        "Where can I find a special student care centre for my child?",
    ],
    "Training & Employment": [
        "What employment support is available for persons with disabilities?",
        "What is the School-to-Work transition programme?",
        "How can a person with disability find a job in Singapore?",
        "What is the IHL-to-Work programme?",
        "Is there a job shadowing programme for disabled persons?",
        "What training programmes exist for PWDs who want to work?",
        "How does SG Enable help with employment for disabled persons?",
        "Can polytechnic graduates with disabilities get job placement help?",
        "What is the supported employment programme in Singapore?",
    ],
    "Cross-Topic": [
        "I have a disability — what government help is available in Singapore?",
        "My child has autism — what care, transport and education support can I get?",
        "What schemes does SG Enable offer?",
        "I am a caregiver — what support services exist for my disabled family member?",
        "What financial assistance is available for persons with disabilities?",
    ],
    "Out-of-Scope (should be rejected)": [
        "What is the weather in Singapore?",
        "How do I apply for HDB flat?",
        "What are the CPF contribution rates?",
        "Tell me a joke",
        "What are disabilities in other countries?",
    ],
}

def test_query(client: httpx.Client, message: str) -> dict:
    try:
        r = client.post(
            f"{BASE_URL}/query",
            json={"message": message, "history": []},
            timeout=60,
        )
        data = r.json()
        return {
            "in_scope": data.get("is_in_scope", False),
            "score": round(data.get("top_similarity_score", 1.0), 3),
            "refusal": data.get("refusal_reason"),
        }
    except Exception as e:
        return {"in_scope": None, "score": None, "refusal": str(e)}


def main():
    print(f"\nTesting against {BASE_URL}\n")
    print("=" * 80)

    totals = {"responded": 0, "rejected": 0, "error": 0}

    with httpx.Client() as client:
        for category, queries in QUERIES.items():
            print(f"\n{'─' * 80}")
            print(f"  {category}")
            print(f"{'─' * 80}")
            for q in queries:
                result = test_query(client, q)
                if result["in_scope"] is None:
                    status = "ERROR "
                    totals["error"] += 1
                elif result["in_scope"]:
                    status = "✓ RESP "
                    totals["responded"] += 1
                else:
                    status = "✗ REJT "
                    totals["rejected"] += 1

                score = f"dist={result['score']}" if result["score"] is not None else ""
                reason = f"({result['refusal']})" if result["refusal"] else ""
                print(f"  [{status}] {score:12} {reason:20} {q[:65]}")

    print(f"\n{'=' * 80}")
    print(f"  SUMMARY")
    print(f"{'=' * 80}")
    print(f"  ✓ Responded (in scope):  {totals['responded']}")
    print(f"  ✗ Rejected (out scope):  {totals['rejected']}")
    print(f"  ! Errors:                {totals['error']}")
    print(f"  Total tested:            {sum(totals.values())}")
    print()


if __name__ == "__main__":
    main()
