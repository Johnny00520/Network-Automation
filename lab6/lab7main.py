#!/bin/env python3
from flask import Flask, jsonify, request, render_template, redirect, url_for
import getconfig, ospfconfig, diffconfig, migration

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/get_config", methods=['GET'])
def get_config():
    return getconfig.getconfig()

@app.route("/diff_config", methods=['GET'])
def diffConf():
    return diffconfig.diffconfig()

@app.route("/migration", methods=['POST'])
def migrate():
    return migration.migration()

@app.route("/ospfConfig", methods=['POST', 'GET'])
def ospf_config():
    if(request.method == 'GET'):
        return redirect(url_for('ospfConf'))

    if(request.method == 'POST'):
        if('IPaddr2' in request.form):
            username = request.form['username']
            password = request.form['password']
            IPaddr = request.form['IPaddr']
            IPaddr2 = request.form['IPaddr2']
            pid = request.form['pid']
            pid2 = request.form['pid2']
            area_id = request.form['areaID']
            area_id2 = request.form['areaID2']
            loopbackIP = request.form['loopbackIP']
        
            ospfconfig.ospf_config(username, password, IPaddr, IPaddr2, pid, pid2, area_id, area_id2, loopbackIP)
            if(IPaddr == '198.51.101.2' and IPaddr2 == '172.16.1.2'):
                return render_template('ospf_form.html', r2area1=request.form['IPaddr'], r2area0=request.form['IPaddr2'])
            else:
                return render_template('ospf_form.html', r4area1=request.form['IPaddr'], r4area0=request.form['IPaddr2'])
            
        else:
            username = request.form['username']
            password = request.form['password']
            IPaddr = request.form['IPaddr']
            pid = request.form['pid']
            area_id = request.form['areaID']
            loopbackIP = request.form['loopbackIP']
  
            #R1
            if(IPaddr == '198.51.101.1'):
                pingTable = ospfconfig.ospf_config(username, password, IPaddr, None, pid, None, area_id, None, loopbackIP)
                pingTable = pingTable.get_html_string(attributes={'class': 'pingtable'})

                return render_template('ospf_form.html', r1area1=request.form['IPaddr'], pingTable=pingTable)
        
            #R3
            if(IPaddr == '172.16.1.3'):
                ospfconfig.ospf_config(username, password, IPaddr, None, pid, None, area_id, None, loopbackIP)
                return render_template('ospf_form.html', r3area0=request.form['IPaddr'])
            

@app.route('/ospfConf')
def ospfConf():
    return render_template('ospf_form.html')
    

if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1", port=80)

