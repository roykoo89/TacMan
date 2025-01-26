using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Sngty;

public class ExampleCommunicator : MonoBehaviour
{
    public Sngty.SingularityManager mySingularityManager;
    private DeviceSignature myDevice = new DeviceSignature();

    public static ExampleCommunicator Instance { get; private set; }

    bool processing = false;

    void Awake()
    {
        // Ensure only one instance of Communicator exists
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject); // Optional: Persist across scenes
        }
        else
        {
            Destroy(gameObject); // Destroy duplicate instances
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        // List<DeviceSignature> pairedDevices = mySingularityManager.GetPairedDevices();
        //
        // //If you are looking for a device with a specific name (in this case exampleDeviceName):
        // for (int i = 0; i < pairedDevices.Count; i++)
        // {
        //     if (deviceName.Equals(pairedDevices[i].name))
        //     {
        //         myDevice = pairedDevices[i];
        //         Debug.Log("Found device with name: " + myDevice.name);
        //         break;
        //     }
        // }

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
        // if (message == "ChangeToRed")
        // {
        //     CubeManager.Instance.ChangeCubeColor(Color.red);
        // }
        // else if (message == "ChangeToBlue")
        // {
        //     CubeManager.Instance.ChangeCubeColor(Color.blue);
        // }
        
        //the message is 3 floats separated by commas
        string[] splitMessage = message.Split(',');
        if (splitMessage.Length == 3)
        {
            float x = float.Parse(splitMessage[0]);
            float y = float.Parse(splitMessage[1]);
            float z = float.Parse(splitMessage[2]);
            StickSimulation.Instance.SetAngles(x, y, z);
        }
    }

    public void onError(string errorMessage)
    {
        Debug.LogError("Error with Singularity: " + errorMessage);
    }

    public void SendMessageToServer(string msg)
    {
        mySingularityManager.sendMessage(msg, myDevice);
    }

    public void OnCollisionSendOnce(string msg)
    {
        if (!processing)
        {
            Debug.Log($"Hit Face: {msg}");
            StartCoroutine(SendMessageToServerCoroutine(msg));
        }
    }

    IEnumerator SendMessageToServerCoroutine(string msg)
    {
        processing = true;
        SendMessageToServer(msg);
        yield return new WaitForSeconds(0.5f);
        processing = false;
    }
}
