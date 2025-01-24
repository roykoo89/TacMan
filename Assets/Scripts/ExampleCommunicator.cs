using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Sngty;

public class ExampleCommunicator : MonoBehaviour
{
    public Sngty.SingularityManager mySingularityManager;
    public string deviceName = "exampleDeviceName";
    private DeviceSignature myDevice = new DeviceSignature();
    
    // Start is called before the first frame update
    void Start()
    {
        List<DeviceSignature> pairedDevices = mySingularityManager.GetPairedDevices();

        //If you are looking for a device with a specific name (in this case exampleDeviceName):
        for (int i = 0; i < pairedDevices.Count; i++)
        {
            if (deviceName.Equals(pairedDevices[i].name))
            {
                myDevice = pairedDevices[i];
                Debug.Log("Found device with name: " + myDevice.name);
                break;
            }
        }

        if (!myDevice.Equals(default(DeviceSignature)))
        {
            //Do stuff to connect to the device here
            mySingularityManager.ConnectToDevice(myDevice);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            mySingularityManager.ConnectToDevice(myDevice);
        }

        if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            mySingularityManager.DisconnectDevice(myDevice);
        }

        if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            mySingularityManager.sendMessage("Hello from Unity!", myDevice);
        }
    }

    public void onConnected()
    {
        Debug.Log("Connected to device!");
    }

    public void onMessageRecieved(string message)
    {
        Debug.Log("Message recieved from device: " + message);
    }

    public void onError(string errorMessage)
    {
        Debug.LogError("Error with Singularity: " + errorMessage);
    }
}
