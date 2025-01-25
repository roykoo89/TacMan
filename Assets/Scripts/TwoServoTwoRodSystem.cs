using UnityEngine;
using System.Collections.Generic;

[ExecuteAlways]
public class TwoServoTwoRodSystem : MonoBehaviour
{
    // Lengths of the rods
    public float L1a = 5f;
    public float L1b = 10f;
    public float L2a = 5f;
    public float L2b = 10f;

    // Angles (in degrees)
    [Range(0f, 360f)] public float theta1 = 45f;
    [Range(0f, 360f)] public float theta2 = 135f;
    [Range(0f, 360f)] public float phi = 45f;

    // References to Transforms for visualization
    public Transform hinge1;
    public Transform hinge2;
    public Transform connectionPoint;

    // Line renderer for visualizing rods
    public LineRenderer rod1aRenderer;
    public LineRenderer rod1bRenderer;
    public LineRenderer rod2aRenderer;
    public LineRenderer rod2bRenderer;

    // Update function to calculate hinge positions
    void Update()
    {
        // Convert angles to radians
        float theta1Rad = theta1 * Mathf.Deg2Rad;
        float theta2Rad = theta2 * Mathf.Deg2Rad;
        float phiRad = phi * Mathf.Deg2Rad;

        // Compute hinge positions in the Y-Z plane (X = 0)
        float H1_y = L1a * Mathf.Sin(theta1Rad); // Use Y for horizontal displacement
        float H1_z = L1a * Mathf.Cos(theta1Rad); // Use Z for vertical displacement

        float H2_y = L2a * Mathf.Sin(theta2Rad); 
        float H2_z = L2a * Mathf.Cos(theta2Rad); 

        // Find intersection(s) of circles in 2D
        List<Vector2> intersections = FindCircleIntersections(H1_y, H1_z, L1b, H2_y, H2_z, L2b);
        
        if (intersections.Count == 0)
        {
            if (connectionPoint != null)
                connectionPoint.localPosition = Vector3.zero;

            return;
        }

        // Select the best intersection
        Vector2 E = intersections[0];
        if (intersections.Count > 1 && intersections[1].y > E.y)
            E = intersections[1];

        // Apply rotation around Y-axis (rotation in the Y-Z plane is done by adjusting the angle phi)
        Vector3 hinge1Pos = RotatePoint(H1_y, H1_z, phiRad);
        Vector3 hinge2Pos = RotatePoint(H2_y, H2_z, phiRad);
        Vector3 connectionPos = RotatePoint(E.x, E.y, phiRad);

        // Update the positions of hinges and the connection point
        if (hinge1 != null) hinge1.localPosition = hinge1Pos;
        if (hinge2 != null) hinge2.localPosition = hinge2Pos;
        if (connectionPoint != null) connectionPoint.localPosition = connectionPos;

        // Update the LineRenderer positions for visualizing the rods
        if (rod1aRenderer != null)
            SetLineRendererPositions(rod1aRenderer, Vector3.zero, hinge1Pos);

        // Rod1b: Hinge1 to Connection Point
        if (rod1bRenderer != null)
            SetLineRendererPositions(rod1bRenderer, hinge1Pos, connectionPos);

        // Rod2a: Servo to Hinge2
        if (rod2aRenderer != null)
            SetLineRendererPositions(rod2aRenderer, Vector3.zero, hinge2Pos);

        // Rod2b: Hinge2 to Connection Point
        if (rod2bRenderer != null)
            SetLineRendererPositions(rod2bRenderer, hinge2Pos, connectionPos);
    }

    // Helper function to rotate a point in the Y-Z plane around the Y-axis by an angle phi
    private Vector3 RotatePoint(float y, float z, float phiRad)
    {
        float y_rot = y * Mathf.Cos(phiRad) - z * Mathf.Sin(phiRad);
        float z_rot = y * Mathf.Sin(phiRad) + z * Mathf.Cos(phiRad);
        return new Vector3(0f, y_rot, z_rot); // X is always 0 for the Y-Z plane
    }

    // Finds the intersection points between two circles (in the Y-Z plane)
    private List<Vector2> FindCircleIntersections(float y0, float z0, float r0, float y1, float z1, float r1)
    {
        List<Vector2> result = new List<Vector2>();
        
        float dy = y1 - y0;
        float dz = z1 - z0;
        float d = Mathf.Sqrt(dy * dy + dz * dz);

        if (d > (r0 + r1) || d < Mathf.Abs(r0 - r1)) return result;

        float a = (r0 * r0 - r1 * r1 + d * d) / (2f * d);
        float h_sq = r0 * r0 - a * a;
        if (h_sq < 0f) return result;

        float h = Mathf.Sqrt(h_sq);
        float x2 = y0 + (dy * a / d);
        float z2 = z0 + (dz * a / d);

        float rx = -dz * (h / d);
        float rz = dy * (h / d);

        Vector2 p1 = new Vector2(x2 + rx, z2 + rz);
        Vector2 p2 = new Vector2(x2 - rx, z2 - rz);

        result.Add(p1);
        result.Add(p2);
        return result;
    }
    
    /// <summary>
    /// Sets the positions of a LineRenderer between two points.
    /// </summary>
    /// <param name="lr">LineRenderer component.</param>
    /// <param name="start">Start position.</param>
    /// <param name="end">End position.</param>
    private void SetLineRendererPositions(LineRenderer lr, Vector3 start, Vector3 end)
    {
        if (lr == null) return;

        lr.positionCount = 2;
        lr.SetPosition(0, start);
        lr.SetPosition(1, end);
    }

}
