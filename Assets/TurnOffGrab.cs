using Oculus.Interaction;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TurnOffGrab : MonoBehaviour
{
    public GameObject handGrab;

    public void TurnOffffGrab()
    {
        handGrab.SetActive(false);
    }
}
