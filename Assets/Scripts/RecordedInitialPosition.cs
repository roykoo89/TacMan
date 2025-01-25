using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class RecordedInitialPosition : MonoBehaviour
{
    public GameObject ballPosition; // Assign from the Inspector
    public GameObject stickPrefab;
    public TMP_Text countdownText; // Assign a UI Text for countdown

    private bool isRecording = false;

    void Update()
    {
        // Detect Y button press
        if (OVRInput.GetDown(OVRInput.Button.Four)) // Y button on left controller
        {
            if (!isRecording)
                StartCoroutine(RecordFingerTipPosition());
        }
    }

    private IEnumerator RecordFingerTipPosition()
    {
        isRecording = true;

        // Countdown logic
        float countdown = 3f;
        while (countdown > 0)
        {
            countdownText.text = $"Recording in: {Mathf.Ceil(countdown)}";
            yield return new WaitForSeconds(1f);
            countdown -= 1f;
        }
        countdownText.text = "Recording...";

        // Get right index fingertip position
        Transform initialPosition = ballPosition.transform;

        GameObject stick = Instantiate(stickPrefab);

        stick.transform.position = initialPosition.position;
        stick.transform.rotation = initialPosition.rotation;

        ballPosition.SetActive(false);

        // Clear UI and reset
        countdownText.text = "";
        isRecording = false;
    }
}
