from flask import Flask, request, jsonify
from lexer import lexer
from parser import parser

app = Flask(__name__)

...