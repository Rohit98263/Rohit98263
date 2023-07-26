from flask import jsonify
from flask_jwt_extended import get_jwt_identity, decode_token
from utils.loggingConfig import *

revoked_tokens = set()

def check_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens or decode_token(jwt_header + '.' + jwt_payload)["jti"] in revoked_tokens


def revoke_token(token):
    ocr_logger.info("Starting to run revoke token function")
    jti = decode_token(token)['jti']
    if jti in revoked_tokens:
        ocr_logger.warning("Token already revoked")
        return "Token already revoked"
    revoked_tokens.add(jti)
    ocr_logger.info("Token revoked successfully")
    return "Token revoked successfully"


def revoke_token_callback():
    ocr_logger.info("Token has been revoked")
    return jsonify({"msg": "Token has been revoked"}), 401