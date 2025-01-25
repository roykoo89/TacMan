using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class RecordedInitialPosition : MonoBehaviour
{
    public GameObject ballPosition; // Assign from the Inspector
    public GameObject stickPrefab;

    private bool isButtonPressed = false;

    void Update()
    {
        // Detect Y button press
        if (OVRInput.GetDown(OVRInput.Button.Four)) // Y button on left controller
        {
            if (!isButtonPressed)
                RecordTipPosition();
        }
    }

    private void RecordTipPosition()
    {
        isButtonPressed = true;

        // Get right index fingertip position
        Transform initialPosition = ballPosition.transform;

        GameObject stick = Instantiate(stickPrefab);

        stick.transform.position = initialPosition.position;
        stick.transform.rotation = initialPosition.rotation;

        ballPosition.SetActive(false);

        isButtonPressed = false;
    }
}
