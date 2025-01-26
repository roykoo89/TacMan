
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelCollision : MonoBehaviour
{
    [SerializeField] private ExampleCommunicator _exampleCommunicator;
    [SerializeField] private AudioSource _audioSource;
    //[SerializeField] private ParticleSystem _particleSystem;
    [SerializeField] private GameObject VoxelDestroyedPrefab;
    [SerializeField] private GameObject playerHeadset;

    private bool stopPlayEffects = false;
    
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Voxel"))
        {
            // Destroy or deactivate the voxel
            //other.gameObject.SetActive(false);

            // Instantiate a destroyed voxel at x times the amount but x time smaller
            int amount = 2;
            for(int i = 0; i < amount; i++)
            {
                GameObject destroyedVoxel = Instantiate(VoxelDestroyedPrefab, other.transform.position, Quaternion.identity);
                destroyedVoxel.transform.localScale = other.transform.localScale/2;
                //add force towards the player
                destroyedVoxel.GetComponent<Rigidbody>().AddForce((playerHeadset.transform.position - destroyedVoxel.transform.position).normalized, ForceMode.Impulse);
                Destroy(destroyedVoxel, 2f);
            }
            
            if (!stopPlayEffects)
            {
                _audioSource.Play();
                // _particleSystem.gameObject.transform.position = other.transform.position;
                // _particleSystem.Play();
                stopPlayEffects = true;
                StartCoroutine(TriggerHapticFeedback());
                StartCoroutine(ResetEffects());
            }
        }
    }
    
    private IEnumerator TriggerHapticFeedback()

    {

        OVRInput.SetControllerVibration(1, 1, OVRInput.Controller.RTouch);

        yield return new WaitForSeconds(0.3f);

        OVRInput.SetControllerVibration(0, 0, OVRInput.Controller.RTouch);

    }
    
    //coroutine to check every 3 seconds if there is no collision with any voxel, if so allow to play the sound and particle again
    IEnumerator ResetEffects()
    {
        yield return new WaitForSeconds(0.5f);
        stopPlayEffects = false;
    }
}
