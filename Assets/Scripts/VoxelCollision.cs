using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelCollision : MonoBehaviour
{
    [SerializeField] private ExampleCommunicator _exampleCommunicator;
    [SerializeField] private AudioSource _audioSource;
    [SerializeField] private ParticleSystem _particleSystem;

    private bool stopPlayEffects = false;
    
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Voxel"))
        {
            // Destroy or deactivate the voxel
            other.gameObject.SetActive(false);

            if (!stopPlayEffects)
            {
                _audioSource.Play();
                _particleSystem.gameObject.transform.position = other.transform.position;
                _particleSystem.Play();
                stopPlayEffects = true;
                StartCoroutine(ResetEffects());
            }

            _exampleCommunicator.SendMessageToServer("ResistMe");
        }
    }
    
    //coroutine to check every 3 seconds if there is no collision with any voxel, if so allow to play the sound and particle again
    IEnumerator ResetEffects()
    {
        yield return new WaitForSeconds(0.5f);
        stopPlayEffects = false;
    }
}
