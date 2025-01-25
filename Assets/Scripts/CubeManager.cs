using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeManager : MonoBehaviour
{
    private static CubeManager instance;

    private GameObject cube;
    
    public static CubeManager Instance
    {
        get
        {
            if (instance == null)

            {
                instance = FindObjectOfType<CubeManager>();
                DontDestroyOnLoad(instance.gameObject);
            }
            return instance;
        }
    }

    public void ChangeCubeColor(Color color)
    {
        cube.GetComponent<Renderer>().material.color = color;
    }
    
    public void SetCube(GameObject cubeObject)
    {
        cube = cubeObject;
    }
}
