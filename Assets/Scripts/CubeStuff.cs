using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeStuff : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        CubeManager.Instance.SetCube(gameObject);
    }
}
