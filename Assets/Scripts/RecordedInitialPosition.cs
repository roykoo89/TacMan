using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class RecordedInitialPosition : MonoBehaviour
{
    public GameObject ballPosition; // Assign from the Inspector
    public GameObject stickPrefab;
    public GameObject leftHand;

    private GameObject _stick;

    private bool isButtonPressed = false;
    
    public void RecordInitialPosition()
    {
        if (!isButtonPressed)
        {
            RecordTipPosition();
        }
    }

    private void RecordTipPosition()
    {
        isButtonPressed = true;

        // Get right index fingertip position
        Transform initialPosition = ballPosition.transform;

        if (_stick == null)
        {
            _stick = Instantiate(stickPrefab);
        }
        else
        {
            _stick.SetActive(true);
        }

        _stick.transform.position = initialPosition.position;
        _stick.transform.rotation = initialPosition.rotation;

        ballPosition.SetActive(false);

        isButtonPressed = false;
    }
    
    public void ResetPosition()
    {
        if (_stick != null)
        {
            _stick.SetActive(false);
        }

        ballPosition.SetActive(true);
        ballPosition.transform.position = leftHand.transform.position;
    }
}
