using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class LaunchArcRender : MonoBehaviour {

    //public GameObject basketBall;

    LineRenderer lr;

    public float velocity;
    public float angle;
    public int resolution;
    public static bool isShooting;
    public static Vector3 startArcPosition;
    public GameObject basketBall;

    float gravity; //force on y axis
    float radianAngle;
    public static Vector3[] arcArray;

    void Awake(){
        lr = GetComponent<LineRenderer>();
        gravity = Mathf.Abs(Physics.gravity.y); 
    }

    void Start()
    {
        isShooting = false;
        arcArray = new Vector3[resolution + 1];

    }

    void Update()
    {
        if (isShooting || !isShooting)
        {
            //ShootBall(CalculateArcArray());
        }

        if (Input.GetKeyDown("space"))
        {
            isShooting = true;
        }

        RenderArc();

    }

    //populating the line renderer with the appropriate settings
    void RenderArc()
    {
        lr.positionCount = resolution + 1;
        lr.SetPositions(CalculateArcArray());
    }

    //create an array of vector 3 positions for the arc
    Vector3[] CalculateArcArray()
    {
        

        radianAngle = Mathf.Deg2Rad * angle;
        float maxDistance = (Mathf.Pow(velocity, 2) * Mathf.Sin(2 * radianAngle)) / gravity;

        for (int i = 0; i <= resolution; i++)
        {
            float t = (float)i / resolution;
            arcArray[i] = CalculateArcPoint(t, maxDistance);
        }

        return arcArray;
    }

    //Calculate the hight and distance of each vertex 
    Vector3 CalculateArcPoint(float t, float maxDistance)
    {
        float x = t * maxDistance;
        float y = (x * Mathf.Tan(radianAngle)) - ((gravity * x * x)/(2 * velocity * velocity * Mathf.Cos(radianAngle) * Mathf.Cos(radianAngle)));

        return new Vector3(x + startArcPosition.x, y + startArcPosition.y, startArcPosition.z);
    }

    /*
    void ShootBall(Vector3[] path)
    {
        isShooting = false;
        int current = 0;

        if (basketBall.transform.position != path[current])
        {
            Vector3 pos = Vector3.MoveTowards(basketBall.transform.position, path[current], velocity * Time.deltaTime);
            Debug.Log("Target Vector " + path[current]);
            Debug.Log("pos" + pos);
            basketBall.GetComponent<Rigidbody>().MovePosition(pos);
        }
        else current = (current + 1) % path.Length;
    }
    */
}
