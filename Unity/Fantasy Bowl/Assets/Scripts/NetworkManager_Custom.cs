using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;

public class NetworkManager_Custom : NetworkManager {

    public TextMeshProUGUI ipAddressText;
	
	public void StartupHost()
    {
        SetPort();
        singleton.StartHost();
    }
    
    public void JoinGame()
    {
        SetIPAddress();
        SetPort();
        singleton.StartClient();
    }

    void SetIPAddress()
    {
        string ipAddress = ipAddressText.text;
        singleton.networkAddress = ipAddress; 
    }

    void SetPort()
    {
        singleton.networkPort = 7777;
    }
}
