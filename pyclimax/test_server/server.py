import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.

json_ret = {
    "senrows": [
            {
                "area": 1,
                "zone": 19,
                "type": 11,
                "type_f": "Smoke Detector",
                "name": "",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 9",
                "status": "",
                "id": "RF:4d364f40",
                "su": 1
            },
            {
                "area": 1,
                "zone": 3,
                "type": 2,
                "type_f": "Remote Controller",
                "name": "",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "N/A",
                "status": "",
                "id": "RF:6ecb0100",
                "su": 0
            },
            {
                "area": 1,
                "zone": 7,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Uterum",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Good, 4",
                "status": "Off, 0.0W",
                "id": "ZB:0000000000000b0f",
                "su": 1
            },
            {
                "area": 1,
                "zone": 1,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Arbetsrum fönster",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 8",
                "status": "Off, 0.0W",
                "id": "ZB:0000000000003137",
                "su": 1
            },
            {
                "area": 1,
                "zone": 20,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Vinställ",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 6",
                "status": "Off, 0.0W",
                "id": "ZB:0000000000004bb4",
                "su": 1
            },
            {
                "area": 1,
                "zone": 15,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Niklas",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Weak, 3",
                "status": "Off, 0.0W",
                "id": "ZB:0000000000006b07",
                "su": 1
            },
            {
                "area": 1,
                "zone": 4,
                "type": 20,
                "type_f": "Temperature Sensor",
                "name": "Vardagsrum",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Good, 5",
                "status": "21.25 °C",
                "id": "ZB:0000000000006e3b",
                "su": 1
            },
            {
                "area": 1,
                "zone": 5,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Annas rum",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Weak, 3",
                "status": "Off, 0.0W",
                "id": "ZB:0000000000007617",
                "su": 1
            },
            {
                "area": 1,
                "zone": 6,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Vardagsrum fönster",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Good, 5",
                "status": "Off, 0.0W",
                "id": "ZB:0000000000008662",
                "su": 1
            },
            {
                "area": 1,
                "zone": 14,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Sofflampa höger",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 7",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000ba32",
                "su": 1
            },
            {
                "area": 1,
                "zone": 18,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Övre hall bordslampa",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Good, 5",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000c1de",
                "su": 1
            },
            {
                "area": 1,
                "zone": 13,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Sofflampa vänster",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 6",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000cd2a",
                "su": 1
            },
            {
                "area": 1,
                "zone": 11,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Köket skänk",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 6",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000cff9",
                "su": 1
            },
            {
                "area": 1,
                "zone": 8,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Övre hall fönster",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Weak, 3",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000d692",
                "su": 1
            },
            {
                "area": 1,
                "zone": 16,
                "type": 52,
                "type_f": "UPIC",
                "name": "",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 8",
                "status": "",
                "id": "ZB:000000000000ee31",
                "su": 1
            },
            {
                "area": 1,
                "zone": 10,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Övre hall golvlampa",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 6",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000f911",
                "su": 1
            },
            {
                "area": 1,
                "zone": 2,
                "type": 48,
                "type_f": "Power Switch Meter",
                "name": "Sovrum",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Strong, 8",
                "status": "Off, 0.0W",
                "id": "ZB:000000000000f9f9",
                "su": 1
            },
            {
                "area": 1,
                "zone": 17,
                "type": 20,
                "type_f": "Temperature Sensor",
                "name": "Övre hall",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "Weak, 3",
                "status": "22.75 °C",
                "id": "ZB:000000000000ff19",
                "su": 1
            },
            {
                "area": 1,
                "zone": 12,
                "type": 50,
                "type_f": "Power Meter",
                "name": "Elmätare",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "N/A",
                "status": "29945.742kWh",
                "id": "ZW:00000006",
                "su": 0
            },
            {
                "area": 1,
                "zone": 21,
                "type": 53,
                "type_f": "Dimmer",
                "name": "Vardagsrum",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "N/A",
                "status": "Off",
                "id": "ZW:00000007",
                "su": 0
            },
            {
                "area": 1,
                "zone": 22,
                "type": 53,
                "type_f": "Dimmer",
                "name": "Bokhylla",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "N/A",
                "status": "On (84%)",
                "id": "ZW:00000008",
                "su": 0
            },
            {
                "area": 1,
                "zone": 23,
                "type": 53,
                "type_f": "Dimmer",
                "name": "Arbetsrum",
                "cond": "",
                "cond_ok": "1",
                "battery": "",
                "battery_ok": "1",
                "tamper": "",
                "tamper_ok": "1",
                "bypass": "No",
                "rssi": "N/A",
                "status": "Off",
                "id": "ZW:00000009",
                "su": 0
            }
    ]
}

welcome_ret = {
    "updates": {
        "version": "HPGW 0.0.1.77 HPGW-L2-XA12 2.1.2.3.1",
        "em_ver": "0.0.1.77",
        "rf_ver": "HPGW-L2-XA12",
        "zb_ver": "2.1.2.3.1",
        "zw_ver": "Z-Wave 3.40",
        "gsm_ver": "Cinterion BGS3 REVISION 01.000",
        "cfg_ver": "1.0",
        "publicip": "81.234.122.159",
        "ip": "192.168.1.226",
        "mac": "00:1D:94:02:C3:EE"
    }
}

post_return = {
    "result": 1,
    "message": "Updated successfully."
}


@app.route('/', methods=['GET'])
def home():
    return '''<h1>HEJ JACQUELINE</h1>
<p>Detta är en server för att visa att jag kan.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/action/deviceListGet', methods=['GET'])
def api_list_get():
    return jsonify(json_ret)

# A route to return all of the available entries in our catalog.
@app.route('/action/welcomeGet', methods=['GET'])
def api_welcome_get():
    return jsonify(welcome_ret)

# A route to return all of the available entries in our catalog.
@app.route('/action/deviceSwitchPSSPost', methods=['POST'])
def api_switch_post():
    query_params = request.form

    id = query_params.get('id')
    switch = query_params.get('switch')

    senrows = json_ret.get('senrows')

    for device in senrows:
        if id in device.get('id'):
            if '1' in switch:
                print('Setting to on"')
                device['status'] = "On, 1.3W"
            else:
                print('Setting to off"')
                device['status'] = "Off, 0.0W"
            break

    return jsonify(post_return)

# A route to return all of the available entries in our catalog.
@app.route('/action/deviceSwitchDimmerPost', methods=['POST'])
def api_dimmer_post():
    query_params = request.form

    id = query_params.get('id')
    level = query_params.get('level')

    senrows = json_ret.get('senrows')

    for device in senrows:
        if id in device.get('id'):
            device['status'] = "On ({0}%)".format(level)
            break

    return jsonify(post_return)

app.run()