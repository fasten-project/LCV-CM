from LCVlib.verify import retrieveOutboundLicense, CompareSPDX, CompareSPDXFlag, CompareSPDX_OSADL, Compare_OSADL, Compare_OSADLFlag
from LCVlib.SPDXIdMapping import ConvertToSPDX, IsAnSPDX
import logging
import signal
import time
from dotenv import load_dotenv
from os import environ, path
import os
from flask import request, jsonify, render_template, url_for#,redirect
import subprocess
import re
from subprocess import check_output
import flask
import argparse
import sys
'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''
# Load .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
# Load parametrs from .env file
PATH = environ.get('PATH')
LOGFILE = environ.get('LOGFILE')
PORT = environ.get('PORT')
HOST = environ.get('HOST')
GITREPO = environ.get('GITREPO')
SHUTDOWN = environ.get('SHUTDOWN')
# API Shutdown function
PID = os.getpid()


def shutdown(secs):
    print("Shutting down server in:")
    for i in range(int(secs), 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    os.kill(int(PID), signal.SIGINT)


# Check the port number range
class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 0 < values < 2**16:
            raise argparse.ArgumentError(
                self, "port numbers must be between 0 and 65535")
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port",
                    help='Port number to connect to',
                    dest='port',
                    # default=PORT,
                    type=int,
                    action=PortAction,
                    metavar="{0..65535}")
parser.add_argument("-P", "--PATH",
                    help='PATH environment override',
                    dest='PATH',
                    # default=environ.get('PYTHONHOME'),
                    type=str)
parser.add_argument("-s", "--shutdown",
                    help='shutdown timer express in seconds',
                    dest='shutdown',
                    # default="SHUTDOWN",
                    type=str)
args = parser.parse_args()
if args.port:
    PORT = args.port
if args.PATH:
    PATH = args.PATH
if args.shutdown:
    SHUTDOWN = args.shutdown
os.environ['PATH'] = PATH



app = flask.Flask(__name__)
app.config["DEBUG"] = True
# logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)


@app.route('/APIEndpoints')
def APIEndpoints():
    return render_template('APIEndpoints.html')


@app.route('/GitHubOutboundLicense')
def Outb():
    return render_template('outbound.html')


@app.route('/GitHubOutboundLicenseOutput', methods=['POST', 'GET'])
def GitHubOutboundLicense():
    if request.method == 'POST':
        url = request.form['url']
        OutboundLicense = retrieveOutboundLicense(url)
        return OutboundLicense


@app.route('/CompatibilitySPDX')
def CompatibilitySPDX():
    return render_template('compatibilitySPDX.html')


@app.route('/CompatibilitySPDXOutput', methods=['POST', 'GET'])
def ComplianceSPDX():
    if request.method == 'POST':
        InboundLicenses = request.form['inboundLicenses']
        InboundLicenses = InboundLicenses.split(",")
        OutboundLicense = request.form['outboundLicense']
        verificationList = CompareSPDX(InboundLicenses, OutboundLicense)
        return jsonify(verificationList)


@app.route('/CompatibilitySPDX_OSADL')
def CompatibilitySPDX_OSADL():
    return render_template('compatibilitySPDX_OSADL.html')


@app.route('/CompatibilitySPDX_OSADLOutput', methods=['POST', 'GET'])
def ComplianceSPDX_OSADL():
    if request.method == 'POST':
        InboundLicenses = request.form['inboundLicenses']
        InboundLicenses = InboundLicenses.split(",")
        OutboundLicense = request.form['outboundLicense']
        verificationList = CompareSPDX_OSADL(InboundLicenses, OutboundLicense)
        return jsonify(verificationList)


@app.route('/CompatibilitySPDXFlag')
def CompatibilitySPDXFlag():
    return render_template('compatibilitySPDXFlag.html')


@app.route('/CompatibilitySPDXFlagOutput', methods=['POST', 'GET'])
def ComplianceSPDXFlag():
    if request.method == 'POST':
        InboundLicenses = request.form['inboundLicenses']
        InboundLicenses = InboundLicenses.split(",")
        OutboundLicense = request.form['outboundLicense']
        verificationFlag = CompareSPDXFlag(InboundLicenses, OutboundLicense)
        # print(verificationList)
        return jsonify(verificationFlag)


@app.route('/GetGitHubOutboundLicense', methods=['POST', 'GET'])
def GetGitHubOutboundLicense():
    args = request.args
    url = args['url']
    OutboundLicense = retrieveOutboundLicense(url)
    return OutboundLicense


@app.route('/LicensesInputSPDX', methods=['GET', 'POST'])
# @app.route('/LicensesInput', methods=['POST'])
def LicensesInputSPDX():
    args = request.args
    # print(args)  # For debugging
    InboundLicenses = args['InboundLicenses']
    InboundLicenses = InboundLicenses.split(",")
    OutboundLicense = args['OutboundLicense']
    verificationList = CompareSPDX(InboundLicenses, OutboundLicense)
    return jsonify(verificationList)


@app.route('/LicensesInputSPDX_OSADL', methods=['POST', 'GET'])
def LicensesInputSPDX_OSADL():
    args = request.args
    print(args)  # For debugging
    InboundLicenses = args['InboundLicenses']
    InboundLicenses = InboundLicenses.split(",")
    OutboundLicense = args['OutboundLicense']
    verificationList = CompareSPDX_OSADL(InboundLicenses, OutboundLicense)
    return jsonify(verificationList)

#this endpoint perform the check upon the OSADL.csv
@app.route('/LicensesInput', methods=['POST', 'GET'])
def LicensesInput():
    args = request.args
    print(args)  # For debugging
    InboundLicenses = args['InboundLicenses']
    #InboundLicenses = InboundLicenses.split(";")
    InboundLicenses = re.split(';|OR', InboundLicenses)
    OutboundLicense = args['OutboundLicense']
    verificationList = Compare_OSADL(InboundLicenses, OutboundLicense)
    return jsonify(verificationList)

@app.route('/LicensesInputFlag', methods=['POST', 'GET'])
def LicensesInputFlag():
    args = request.args
    print(args)  # For debugging
    InboundLicenses = args['InboundLicenses']
    InboundLicenses = InboundLicenses.split(";")
    OutboundLicense = args['OutboundLicense']
    verificationList = Compare_OSADLFlag(InboundLicenses, OutboundLicense)
    return jsonify(verificationList)


@app.route('/ConvertToSPDX', methods=['POST', 'GET'])
def ConvertToSPDXEndpoint():
    args = request.args
    print(args)  # For debugging
    VerboseLicense = args['VerboseLicense']
    SPDXid=ConvertToSPDX(VerboseLicense)
    return jsonify(SPDXid)

@app.route('/IsAnSPDX', methods=['POST', 'GET'])
def IsAnSPDXEndpoint():
    args = request.args
    print(args)  # For debugging
    SPDXid = args['SPDXid']
    Bool=IsAnSPDX(SPDXid)
    if Bool is None:
        Bool = False
    return jsonify(Bool)



@app.route('/LicensesInputSPDXFlag', methods=['GET', 'POST'])
# @app.route('/LicensesInput', methods=['POST'])
def LicensesInputSPDXFlag():
    args = request.args
    InboundLicenses = args['InboundLicenses']
    InboundLicenses = InboundLicenses.split(",")
    OutboundLicense = args['OutboundLicense']
    verificationFlag = CompareSPDXFlag(InboundLicenses, OutboundLicense)
    return jsonify(verificationFlag)



@app.route('/shutdown/', defaults={"secs": "1"})
@app.route('/shutdown/<secs>')
def shutd(secs):
    shutdown(int(secs))
    return "Shutting down server"


@app.route('/PATH', methods=['GET'])
def path():
    CurrentPath = os.getenv("PATH")
    return str(CurrentPath)


f = open("serverParameters/PORT.txt", "w")
f.write(str(PORT))
f.close()
f = open("shutdown.txt", "w")
f.write("SHUTDOWN="+str(SHUTDOWN)+"\n")
f.close()
# PID = os.getpid()
f = open("shutdown.txt", "a")
f.write("PID="+str(PID))
f.close()

limit = -1
SHUTDOWN = int(SHUTDOWN)
if SHUTDOWN > limit:
    subprocess.Popen(["python3", "server_shutdown.py"])

app.run(host=HOST, port=PORT)
