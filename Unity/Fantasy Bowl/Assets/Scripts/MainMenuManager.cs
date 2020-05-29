using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainMenuManager : MonoBehaviour {

    public GameObject mainMenu;
    public GameObject multiplaterMenu;
    public GameObject optionsMenu;


	void Awake () {
        mainMenu.SetActive(true);
        multiplaterMenu.SetActive(false);
        optionsMenu.SetActive(false);
	}

    public void OnClickMultiplayer()
    {
        mainMenu.SetActive(false);
        multiplaterMenu.SetActive(true);
    }

    public void OnClickOptions()
    {
        mainMenu.SetActive(false);
        optionsMenu.SetActive(true);
    }

    public void OnClickBack()
    {
        mainMenu.SetActive(true);
        multiplaterMenu.SetActive(false);
        optionsMenu.SetActive(false);
    }
	
    public void OnClickExit()
    {
        Application.Quit();
    }
}
