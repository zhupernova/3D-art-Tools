#Light Manager
#Gets a list of standard lights in the scene
#and lets the user change the color and intensity
#also lets the user delete, rename and copy the scene lights as well



import maya.cmds as cmds
import sys



class lightManagerFunctions():

    def __init__(self):
        pass


#get list of lights
#make a list/array of light types. add a function depending on the light type selected

    def standardLights(self):

        lightsList = []
        lightStr = 'Light'

        lightList = cmds.ls(lights=True,shapes=True)

        for lights in lightList:
            sceneLights = cmds.nodeType(lights)

            if lightStr in sceneLights:
                lightsList.append(lights)

        return lightsList

        return "Error"


    def setLightIntensity(self,light,intensity):
        cmds.setAttr(light + '.intensity', intensity)

    def getLightIntensity(self,light):
        gLIntensity = cmds.getAttr(light + '.intensity')
        return gLIntensity

    def setLightColor(self,light,color):
        cmds.setAttr(light + '.color', color[0],color[1],color[2],type="double3")

    def lightName(self,light,name):
        cmds.rename(light,name)

    def setShadowColor(self,light,shadowColor):
        cmds.setAttr(light + '.shadowColor', shadowColor[0],shadowColor[1],shadowColor[2],type="double3")

    def spotLightPenumbraAngle(self,sLight,penumbra):
        cmds.setAttr(sLight + '.penumbraAngle', penumbra)

    def spotLightConeAngle(self,sLight,cone):
        cmds.setAttr(sLight + '.coneAngle',cone)

    def spotLightDropOff(self,sLight,dropoff):
        cmds.setAttr(sLight + '.dropoff',dropoff)

    def ambientLightShade(self,aLight,aShade):
        cmds.setAttr(aLight + '.ambientShade',aShade)


class LightUI():

    def __init__(self):

        self.lmFunc = lightManagerFunctions()

        if cmds.window('LightManager', exists=True):
            cmds.deleteUI('LightManager')

    def mainWindow(self):

        self.lightManagerWindow = cmds.window('LightManager', widthHeight=(700,1000),menuBar = True,sizeable=False)


        #Menu Items
        self.editMenu = cmds.menu('editMenu', label='Edit')
        cmds.menuItem(label="Save Settings", parent=self.editMenu)
        cmds.menuItem(label="Reset Settings", parent=self.editMenu)

        self.helpMenu = cmds.menu('helpMenu', label='Help')
        cmds.menuItem(label="Help on Tool", parent=self.helpMenu)


        #Main Layout
        self.mainLayout = cmds.formLayout('MainLayout')
        self.backFrame = cmds.scrollLayout('backFrame',hst = 16,vst = 16,borderVisible=True)
        cmds.formLayout('MainLayout', edit=True, attachForm = ((self.backFrame,'top',0),
                                                               (self.backFrame,'left',0),
                                                               (self.backFrame,'right',0),
                                                               (self.backFrame, 'bottom', 0)))

        self.secondForm = cmds.formLayout('secondForm',nd = 100,parent=self.backFrame)
        self.lightList = cmds.textScrollList('LightList',numberOfRows = 18, width = 250, height = 500,parent = self.secondForm, sc = self.lightControls)
        self.refreshButton = cmds.button('RefreshLightList',width = 123,label="Refresh Light List")
        self.renameButton = cmds.button('Rename',label='Rename',width=118)
        self.deleteButton = cmds.button('Delete',label='Delete',width=123)
        self.copyLightButton = cmds.button('Copy', label='Copy Light',width=118)
        self.closeButton = cmds.button('Close', label='Close',width=118)


        self.commonAttrs = cmds.frameLayout('Common Attributes', width = 360,height=155, marginHeight = 3, collapsable=False, enable=False, visible=True, parent=self.secondForm)
        self.lightRename = cmds.textFieldGrp('Rename',label='Rename', width = 100,columnWidth2 = (79,275), columnAttach = (1,'right',2),parent=self.commonAttrs)
        self.lightIntensity = cmds.floatSliderGrp('Intensity', label='Intensity', field=True, minValue=0.000, maxValue=10.000, value=1.000, step=0.001, width=20, columnAttach = (1,'right',5),columnWidth3 = (80,50,140),dragCommand = self.intensityIntSlider)
        self.lightColor = cmds.colorSliderGrp('ColorSlider',label='Light Color',width=20,columnAttach = (1,'right',5), columnWidth3 = (80,50,140),dragCommand = self.lightColorSlider)
        self.shadowColor = cmds.colorSliderGrp('ShadowSlider', label = 'Shadow Color', width=20,columnAttach = (1,'right',5), columnWidth3 = (80,50,140), dragCommand = self.shadowColorSlider)
        self.illumByDefault = cmds.checkBox('illumByDefault', label = 'Illuminate by Default')

        #ambientMenu
        self.ambientMenu = cmds.frameLayout('Ambient Light Attributes',width = 360,collapsable=False,visible=False,parent=self.secondForm)
        self.ambientShade = cmds.floatSliderGrp('ambShade', label = 'Ambient Shade', field=True,minValue= 0.000, maxValue = 1.000, value=0.500, step = 0.001, width =20, columnAttach = (1,'right',5),columnWidth3 = (84,50,140), parent = self.ambientMenu, dragCommand = self.ambientShadeControls)

        #directionalMenu
        self.directionalMenu = cmds.frameLayout('Directional Light Attributes', width = 360,collapsable=False,visible=False,parent=self.secondForm)
        self.eDirectionalDiffuseCheckBox = cmds.checkBox('EmitDiffuse', label='Emit Diffuse')
        self.eDirectionalSpecular = cmds.checkBox('Emit Specular', label='Emit Specular')

        #pointMenu
        self.pointMenu = cmds.frameLayout('Point Light Attributes', width = 360, collapsable=False,visible=False,parent=self.secondForm)
        self.ePointDiffuseCheckBox = cmds.checkBox('EmitDiffuse', label= 'Emit Diffuse')
        self.ePointSpecular = cmds.checkBox('Emit Specular',label='Emit Specular')

        # spotMenu
        self.spotMenu = cmds.frameLayout('Spot Light Attributes', width=360, collapsable=False, visible=False, marginHeight = 5, parent=self.secondForm)
        self.spotCone = cmds.floatSliderGrp('coneAngle', label ='Cone Angle', field=True, minValue = 0.500, maxValue = 179.500, value = 40.000, step = 0.001, width=20,columnAttach = (1,'right',5),columnWidth3 = (84,50,140), parent=self.spotMenu,  dragCommand = self.spotLightConeAngleControls)
        self.spotPenum = cmds.floatSliderGrp('penumAngle', label='Penumbra', field=True, minValue=-10.000, maxValue=10.000, value=0.000, step=0.001, width=20, columnAttach = (1,'right',5),columnWidth3 = (84,50,140), parent=self.spotMenu, dragCommand = self.spotLightPenumAngleControls)
        self.spotDropOff = cmds.floatSliderGrp('dropOff', label = 'Dropoff', field=True,minValue = 0.000, maxValue = 255.000, value = 0.000, step = 0.001,width=20, columnAttach = (1,'right',5),columnWidth3 = (84,50,140), parent=self.spotMenu, dragCommand = self.spotLightDropoffControls)

        #areaMenu
        self.areaMenu = cmds.frameLayout('Area Light Attributes', width = 360, collapsable=False,visible=False,parent=self.secondForm)
        self.eAreaDiffuseCheckBox = cmds.checkBox('EmitDiffuse', label='Emit Diffuse')
        self.eAreaSpecular = cmds.checkBox('Emit Specular', label='Emit Specular')

        #volumeMenu
        self.volumeMenu = cmds.frameLayout('Volume Light Attributes', width = 360, collapsable=False,visible=False,parent=self.secondForm)
        self.eVolumeDiffuseCheckBox = cmds.checkBox('EmitDiffuse', label='Emit Diffuse')
        self.eVolumeSpecular = cmds.checkBox('Emit Specular', label='Emit Specular')

        cmds.formLayout('secondForm', edit=True, attachForm = ((self.lightList, 'top', 20),
                                                               (self.lightList, 'left', 5),
                                                               (self.commonAttrs,'top',20),
                                                               (self.commonAttrs,'left',260),
                                                               (self.ambientMenu, 'top', 175),
                                                               (self.ambientMenu, 'left', 260),
                                                               (self.directionalMenu, 'top', 175),
                                                               (self.directionalMenu, 'left', 260),
                                                               (self.pointMenu, 'top', 175),
                                                               (self.pointMenu, 'left', 260),
                                                               (self.spotMenu, 'top', 175),
                                                               (self.spotMenu, 'left', 260),
                                                               (self.areaMenu, 'top', 175),
                                                               (self.areaMenu, 'left', 260),
                                                               (self.volumeMenu, 'top', 175),
                                                               (self.volumeMenu, 'left', 260),
                                                               (self.refreshButton,'bottom',5),
                                                               (self.refreshButton,'left',5),
                                                               (self.renameButton,'bottom',5),
                                                               (self.renameButton, 'left', 260),
                                                               (self.deleteButton, 'bottom', 5),
                                                               (self.deleteButton, 'left', 131),
                                                               (self.copyLightButton, 'bottom', 5),
                                                               (self.copyLightButton, 'left', 380),
                                                               (self.closeButton, 'bottom', 5),
                                                               (self.closeButton, 'left', 500)
                                                               ))

        cmds.button('RefreshLightList', edit=True, command=self.refreshImportedLightList)
        cmds.button('Rename',edit=True,command=self.lightName)
        cmds.button('Delete',edit=True, command = self.deleteLight)
        cmds.button('Copy', edit=True, command=self.copyButton)
        cmds.button('Close', edit=True, command=('cmds.deleteUI(\"' + self.lightManagerWindow + '\", window=True)'))
        cmds.showWindow(self.lightManagerWindow)


    #######################################################################################
    #
    # common UI Elements
    #
    #######################################################################################


    def intensityIntSlider(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
            intensityLight = cmds.floatSliderGrp('Intensity', q=True, value=True)
            self.lmFunc.setLightIntensity(lightN, intensityLight)


    def lightColorSlider(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
            newColor = cmds.colorSliderGrp('ColorSlider',q=True,rgb=True)
            self.lmFunc.setLightColor(lightN, newColor)


    def shadowColorSlider(self, *args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
            newColor = cmds.colorSliderGrp(self.shadowColor, q=True, rgb=True)
            self.lmFunc.setShadowColor(lightN, newColor)


    def lightControls(self,*args):

        lights = cmds.textScrollList(self.lightList, q = True, selectItem = True)

        if len(lights) != 0:
            cmds.frameLayout(self.commonAttrs,edit=True,enable=True)

        selLights = cmds.select(lights)

        self.getIntensityAttr()
        self.getColorAttr()
        self.getShadowColorAttr()

        for light in lights:

            if cmds.nodeType(light) == 'directionalLight':
                cmds.frameLayout(self.directionalMenu,edit=True, visible=True)
            else:
                cmds.frameLayout(self.directionalMenu,edit=True, visible=False)

            if cmds.nodeType(light) == 'ambientLight':
                cmds.frameLayout(self.ambientMenu,edit=True, visible=True)
                self.getambientShadeAttr()
            else:
                cmds.frameLayout(self.ambientMenu,edit=True, visible=False)


            if cmds.nodeType(light) == 'pointLight':
                cmds.frameLayout(self.pointMenu,edit=True, visible=True)
            else:
                cmds.frameLayout(self.pointMenu,edit=True, visible=False)

            if cmds.nodeType(light) == 'spotLight':
                cmds.frameLayout(self.spotMenu,edit=True, visible=True)
                self.getSpotConeAttr()
                self.getSpotPenumAttr()
                self.getSpotDropoffAttr()
            else:
                cmds.frameLayout(self.spotMenu,edit=True, visible=False)


            if cmds.nodeType(light) == 'areaLight':
                cmds.frameLayout(self.areaMenu,edit=True, visible=True)
            else:
                cmds.frameLayout(self.areaMenu,edit=True, visible=False)

            if cmds.nodeType(light) == 'volumeLight':
                cmds.frameLayout(self.volumeMenu,edit=True, visible=True)
            else:
                cmds.frameLayout(self.volumeMenu,edit=True, visible=False)



    #######################################################################################
    #
    # button Controls
    #
    #######################################################################################

    def copyButton(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
            cmds.select(lightN)
            cmds.duplicate()
            self.refreshImportedLightList()


    def refreshImportedLightList(self, *args):

        cmds.textScrollList(self.lightList, e=True, removeAll=True)
        if self.lmFunc.standardLights() != "Error":
            for lights in self.lmFunc.standardLights():
                cmds.textScrollList(self.lightList, e=True, selectIndexedItem=1, append=lights)


    def deleteLight(self, *args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
            cmds.select(lightN)
            cmds.delete()
            self.refreshImportedLightList()


    def lightName(self, *args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
            newName = cmds.textFieldGrp('Rename', q=True, text=True)
            self.lmFunc.lightName(lightN, newName)
            self.refreshImportedLightList()


    #######################################################################################
    #
    # ambientLightControl
    #
    #######################################################################################

    def ambientShadeControls(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
        if cmds.nodeType(lightN) == 'ambientLight':
            ambShade = cmds.floatSliderGrp(self.ambientShade, q=True, value=True)
            self.lmFunc.ambientLightShade(lightN, ambShade)

    #get the attrs for ambientShades
    def getambientShadeAttr(self, *args):

        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            ambShade = cmds.getAttr(light + '.ambientShade')
            cmds.floatSliderGrp('ambShade', e=True, value= ambShade)


    #######################################################################################
    #
    # spotLightControls
    #
    #######################################################################################

    def spotLightConeAngleControls(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
        if cmds.nodeType(lightN) == 'spotLight':
            coneAngle = cmds.floatSliderGrp(self.spotCone, q=True, value=True)
            self.lmFunc.spotLightConeAngle(lightN, coneAngle)


    def spotLightPenumAngleControls(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
        if cmds.nodeType(lightN) == 'spotLight':
            penumAngle = cmds.floatSliderGrp(self.spotPenum, q=True, value=True)
            self.lmFunc.spotLightPenumbraAngle(lightN, penumAngle)


    def spotLightDropoffControls(self,*args):

        if (cmds.textScrollList(self.lightList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            lightN = cmds.textScrollList(self.lightList, q=True, selectItem=True)[0]
        if cmds.nodeType(lightN) == 'spotLight':
            dropoff = cmds.floatSliderGrp(self.spotDropOff, q=True, value=True)
            self.lmFunc.spotLightDropOff(lightN, dropoff)


    #get the attrs of the SpotLight Attrs
    def getSpotConeAttr(self, *args):

        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            coneAngle = cmds.getAttr(light + '.coneAngle')
            cmds.floatSliderGrp('coneAngle', e=True, value= coneAngle)


    def getSpotPenumAttr(self, *args):

        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            penumAngle = cmds.getAttr(light + '.penumbraAngle')
            cmds.floatSliderGrp('penumAngle', e=True, value = penumAngle)


    def getSpotDropoffAttr(self, *args):

        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            dropoff = cmds.getAttr(light + '.dropoff')
            cmds.floatSliderGrp('dropOff', e=True, value = dropoff)


    #######################################################################################
    #
    # get the attr and set that as the setting for the light attr per the light selected
    #
    #######################################################################################

    def getIntensityAttr(self, *args):
        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            intLight = cmds.getAttr(light + '.intensity')
            cmds.floatSliderGrp('Intensity', e=True, value=intLight)


    def getColorAttr(self, *args):
        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            colLight = cmds.getAttr(light + '.color')[0]
            cmds.colorSliderGrp('ColorSlider', e=True, rgb=(colLight[0], colLight[1], colLight[2]))


    def getShadowColorAttr(self, *args):
        light = cmds.ls(sl=True, dag=True)[0]
        if len(light) <= 0:
            return
        else:
            shadLight = cmds.getAttr(light + '.shadowColor')[0]
            cmds.colorSliderGrp('ShadowSlider', e=True, rgb=(shadLight[0], shadLight[1], shadLight[2]))



lightUI = LightUI()
lightUI.mainWindow()




