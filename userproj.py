'''
Created on 21 nov. 2018

@author: thomasgumbricht
'''

from sys import exit
import os
import geoimagine.gis.mj_gis_v80 as mj_gis


class ProcessUserProj:
    '''Class for User, tract and project management'''
    def __init__(self, process,session,verbose): 
        '''The constructor expects an instance of process'''
        self.process = process
        self.session = session
        self.verbose = verbose
        #direct to subprocess

        
        if self.process.proc.processid.lower() == 'managedefregproj':
            '''Creates a project and a tract using a default region and links them, creates a site linked to the tract that is identical to the tract
            '''
            #Check that the rules for tract and project are fulfilled and create the queryD
            '''
            <parameters defaultregion = 'trmm' 
            tractid = 'karttur-trmm' 
            tractname = 'karttur trmm' 
            projid = 'karttur-trmm' 
            projname = 'karttur trmm'>
            <tracttitle>Karttur trmm</tracttitle>
            <tractlabel>Karttur trmm</tractlabel>
            <projtitle>Karttur trmm</projtitle>
            <projlabel>Karttur trmm</projlabel>
            '''
            
            queryD = {}
            tractidparts = self.process.params.tractid.split('-')
            if len(tractidparts) >= 2 and len(tractidparts[0]) >= 4 and len(tractidparts[1]) >= 4:
                queryD['tractid'] = self.process.params.tractid
            else:
                exitstr = 'The usertracid nust contain at laest one hyphen and at least 4 letters on each side of the hyphen'
                exit(exitstr)
            projidparts = self.process.params.projid.split('-')
            if len(projidparts) >= 2 and len(projidparts[0]) >= 4 and len(projidparts[1]) >= 4:
                queryD['projid'] = self.process.params.projid
            else:
                exitstr = 'The projid must contain at least one hyphen and at least 4 letters on each side of the hyphen'
                exit(exitstr)   
            for key in self.process.proc.paramsD:
                queryD[key] = self.process.proc.paramsD[key]
            print (self.process.proc.userProj.userid)
            queryD['userid'] = self.process.proc.userProj.userid #self.process.proc.userProj.userid
            queryD['siteid'] = queryD['tractid']
            queryD['sitename'] = queryD['tractname']
            queryD['sitetitle'] = queryD['tracttitle']
            queryD['sitelabel'] = queryD['tractlabel']
            queryD['regiontype'] = 'D'
                
            self.session._ManageDefRegProjTractSite(queryD)
            
        elif self.process.proc.processid.lower() == 'managetractproj':
            self._ManageTractProject()
            
        
        elif self.process.proc.processid.lower() == 'addprojsite':
            '''Adds a new site to an existing tract in an existing project
            '''
            print (self.process.proc.paramsD)
            queryD = self.process.proc.paramsD
            #add the userid to the query, duplicate tract to site
            queryD['userid'] = self.process.proc.userProj.userid #self.process.proc.userProj.userid
            queryD['siteid'] = self.process.proc.userProj.siteid
            self.session._AddProjSite()
            
        elif self.process.proc.processid.lower() == 'addprojplot':
            '''Adds a new plot to an existing site in an existing tract in an existing project
            '''
            self.session._AddProjPlot()

        elif self.process.proc.processid == 'manageproj':
            pass
            #ConnUserLocale.ManageProj(aD,tD)
        else:
            exitstr = 'No process %s under ProcessUerProject' %(self.process.proc.processid)
            exit(exitstr)
    '''      
    def _CreateTractROI(self,srcFPN):
        REGIONID, NAME, CATEGORY, STRATUM,PARENTID,PARENTCAT
        print (srcFPN)
        pass
    
    def _
    fieldDD = self._SetfieldD( query['regionid'], query['regionname'], query['regioncat'], query['stratum'], query['parentid'], query['parentcat'])
                    layer = self.process.dstLayerD[locus][datum][comp]

                    #The destination region must be forced,this is becuase the locus to be created did not exists when chekcing for the feault locus
                    if self.verbose:
                        print ('        forcing region from to',locus, self.process.proc.paramsD['regionid'])
                    print ('layer.locus',layer.locus.locus)
                    print ('layer.locuspath',layer.locus.path)
                    #layer.locus = self.process.proc.paramsD['regionid']
                    print ('new locus', self.process.proc.paramsD['regionid'])
                    
                    if layer.locus.locus != self.process.proc.paramsD['regionid']:
                        #print (layer.locus.locus,self.process.proc.paramsD['regionid'])
                        #exit('Incorrect locus.locus')
                        layer.locus.locus = self.process.proc.paramsD['regionid']
                    if layer.locus.path != self.process.proc.paramsD['regionid']:
                        #exit('Incorrect locus.path')
                        layer.locus.path = self.process.proc.paramsD['regionid']
                                                                      
                    #layer.locuspath = self.process.proc.paramsD['regionid']
                    layer._SetPath()
                    
                    
                    if self.verbose:
                        print ('        filepath', layer.FPN)
   
                    layer.CreateVectorAttributeDef(fieldDD)
                    layer._SetBounds(query['epsg'],query['minlon'],query['minlat'],query['maxlon'],query['maxlat'])

                    projection = mj_gis.MjProj()
                    projection.SetFromEPSG(query['epsg'])

                    if not layer._Exists() or self.process.proc.overwrite:
                        mj_gis.CreateESRIPolygonPtL(layer.FPN, layer.fieldDefL, layer.BoundsPtL, projection.proj_cs, query['regionid'])          
                    boundsD = mj_gis.GetFeatureBounds(layer.FPN,'REGIONID')
                    
                    #Set lonlat projection
                    lonlatproj = mj_gis.MjProj()
                    lonlatproj.SetFromEPSG(4326)
                    
                    #Get the corners in lonlat
                    llD = mj_gis.ReprojectBounds(layer.BoundsPtL,projection.proj_cs,lonlatproj.proj_cs)

                    session._InsertDefRegion(self.process, layer, query, boundsD[query['regionid']], llD )
    '''
            
    def _ManageTractProject(self):
        '''Manage tract project
        '''
        #check that compid corresponds
        print (self.process.params.compid)
        for locus in self.process.srcLayerD:
            for datum in self.process.srcLayerD[locus]:
                for srccomp in self.process.srcLayerD[locus][datum]:
                    print (self.process.srcLayerD[locus][datum][srccomp].comp.compid)
        if not self.process.params.compid == self.process.srcLayerD[locus][datum][srccomp].comp.compid:
            print ('compid do not match')
            SNULLEBULLE
        #Get the parent of the ancillary region, and compare to given parent in params
        queryD ={'compid':self.process.params.compid}
        #paramL= ['regionid','regioncat']
        parentRegion = self.session._SelectParentRegion(queryD)
        if not parentRegion[0] == self.process.params.defaultregion:
            print ('defaultregion do not match', parentRegion[0], self.process.params.defaultregion)
            SNULLEBULLE
        if not os.path.exists(self.process.srcLayerD[locus][datum][srccomp].FPN):
            exitstr = 'The ancillary region file %(fpn)s does not exist' %{'fpn':self.process.srcLayerD[locus][datum][srccomp].FPN}
            print(exitstr)
            SNULLEBULLE
            exit(exitstr)
        
        self.regionLayer = self._DefaultRegion(self.process.srcLayerD[locus][datum][srccomp],datum,srccomp,parentRegion[1])
  
        queryD = {}
        tractidparts = self.process.params.tractid.split('-')
        if len(tractidparts) >= 2 and len(tractidparts[0]) >= 4 and len(tractidparts[1]) >= 4:
            queryD['tractid'] = self.process.params.tractid
        else:
            exitstr = 'The usertracid must contain at laest one hyphen and at least 4 letters on each side of the hyphen'
            exit(exitstr)
        projidparts = self.process.params.projid.split('-')
        if len(projidparts) >= 2 and len(projidparts[0]) >= 4 and len(projidparts[1]) >= 4:
            queryD['projid'] = self.process.params.projid
        else:
            exitstr = 'The projid must contain at least one hyphen and at least 4 letters on each side of the hyphen'
            exit(exitstr)   
        
        for key in self.process.proc.paramsD:
            queryD[key] = self.process.proc.paramsD[key]
        #print (self.process.proc.userProj.userid)
        queryD['userid'] = self.process.proc.userProj.userid
        queryD['siteid'] = queryD['tractid']
        queryD['sitename'] = queryD['tractname']
        queryD['sitetitle'] = queryD['tracttitle']
        queryD['sitelabel'] = queryD['tractlabel']
        queryD['regiontype'] = 'T'
            
        self.session._ManageTractProjSite(queryD)
                                   
        #Check that the region is s
        #SNULLEBULLE
        #self.session._AddProjTractSite()
        self.regiontype = 'tract'
        if self.process.params.modtilelink:
            
            self._LinkUserRegionToMODIS()
        if self.process.params.mgrstilelink:
            pass
        if self.process.params.wrstilelink:
            pass
        
    def _LinkUserRegionToMODIS(self):
        from geoimagine.modis import ProcessModis
        #Change the dst to the src, and send off to MODIS Process
        process = lambda:None
        process.proc = lambda:None
        process.proc.processid = 'LinkInternalToMODIS'
        
        process.params = lambda:None
        process.params.regionLayer = self.regionLayer
        process.params.regiontype = self.regiontype
        process.params.tractid = self.process.params.tractid


        
        ProcessModis(process, self.session, self.verbose)
        '''
        FPN = self.regionLayer.FPN
        layer = self.regionLayer
        regionid = ''
        regiontype = 'tract'
        session = self.session
        FPN,layer,regionid,session,regiontype
        '''

    
        
    def _DefaultRegion(self,srcLayer,datum,comp,parentcat):
        '''THIS IS A DUPLICATE, SHOULD BE FIXED
        '''
        '''
        <parameter paramid = 'copycomp' paramtyp = 'text' tagorattr = 'Attr' required = 'N' defaultvalue = 'tractproject' ></parameter>
            <parameter paramid = 'defaultregion' paramtyp = 'text' tagorattr = 'Attr' required = 'Y' defaultvalue = '' ></parameter>
            <parameter paramid = 'compid' paramtyp = 'text' tagorattr = 'Attr' required = 'Y' defaultvalue = '' ></parameter>
            <parameter paramid = 'tractid' paramtyp = 'text' tagorattr = 'Attr' required = 'Y' defaultvalue = ''></parameter>
            <parameter paramid = 'tractname' paramtyp = 'text' tagorattr = 'Attr' required = 'Y' defaultvalue = ''></parameter>
            <parameter paramid = 'projid' paramtyp = 'text' tagorattr = 'Attr' required = 'Y' defaultvalue = '' ></parameter>
            <parameter paramid = 'projname' paramtyp = 'text' tagorattr = 'Attr' required = 'Y' defaultvalue = '' ></parameter>
            <parameter paramid = 'projtitle' paramtyp = 'text' tagorattr = 'Tag' required = 'Y' defaultvalue = '' ></parameter>
            <parameter paramid = 'projlabel' paramtyp = 'text' tagorattr = 'Tag' required = 'Y' defaultvalue = '' ></parameter>    
            <parameter paramid = 'tracttitle' paramtyp = 'text' tagorattr = 'Tag' required = 'Y' defaultvalue = '' ></parameter>
            <parameter paramid = 'tractlabel' paramtyp = 'text' tagorattr = 'Tag' required = 'Y' defaultvalue = '' ></parameter>
        '''   
        
        
        dstLayer = self.process.dstLayerD[self.process.params.tractid][datum][comp]
        print (dstLayer.FPN)

        if not dstLayer._Exists() or self.process.proc.overwrite:
            

            
            #fieldDD = self._SetfieldD( query['regionid'], query['regionname'], query['regioncat'], query['stratum'], query['parentid'], query['parentcat'])
            fieldDD = self._SetfieldD( self.process.params.tractid, self.process.params.tractname, 'tract', 12, self.process.params.defaultregion, parentcat)
    
            dstLayer.CreateVectorAttributeDef(fieldDD)
            
            srcLayer._GetBounds()
    
            if srcLayer.spatialRef.epsg == 4326:

                mj_gis.CreateESRIPolygonPtL(dstLayer.FPN, dstLayer.fieldDefL, srcLayer.BoundsPtL, srcLayer.spatialRef.proj_cs, self.process.params.tractid)
                valueL = []
                paramL = ['ullon','ullat','urlon','urlat','lrlon','lrlat','lllon','lllat']
                ptL = [item for sublist in srcLayer.BoundsPtL for item in sublist]
                
                llD =  dict(zip(paramL,ptL))
                bounds = (srcLayer.minx, srcLayer.miny, srcLayer.maxx, srcLayer.maxy)

            else:
                print (srcLayer.spatialRef.epsg)
                GEOTRANSRUN
            
                dstLayer._SetBounds(srcLayer.epsg, minlon,minlat,maxlon,maxlat)
                
                projection = mj_gis.MjProj()
                projection.SetFromEPSG(epsg)
                
                if not dstLayer._Exists() or self.process.proc.overwrite:
                    mj_gis.CreateESRIPolygonPtL(dstLayer.FPN, dstLayer.fieldDefL, dstLayer.BoundsPtL, projection.proj_cs, query['regionid'])          
                boundsD = mj_gis.GetFeatureBounds(layer.FPN,'REGIONID')
                
                #Set lonlat projection
                lonlatproj = mj_gis.MjProj()
                lonlatproj.SetFromEPSG(4326)
                
                #Get the corners in lonlat
                llD = mj_gis.ReprojectBounds(layer.BoundsPtL,projection.proj_cs,lonlatproj.proj_cs)
            print (dstLayer.locus.locus)
            print (dstLayer.comp)
            print (llD)
            #self.process, layer, query, boundsD[query['regionid']], llD 
            #query['regioncat'], query['regionid'], query['regionname'], query['parentid'], query['title'], query['label'])
            query = {'regionvcat':'tract','regionid':self.process.params.tractid,'regionname':self.process.params.tractname,
                     'parentid':self.process.params.defaultregion,'title':self.process.params.tracttitle, 'label':self.process.params.tractlabel,
                     'regioncat':'tract','parentcat':parentcat,'epsg':srcLayer.spatialRef.epsg }
            
            self.session._InsertTractRegion(self.process, dstLayer, query, bounds, llD )
        return dstLayer
     
    def _SetfieldD(self,regionid,regionname,regioncat,stratum,parentid,parentcat):
        #TGTODO SHOULD BE FROM DB
        fieldDD = {}
        fieldDD['REGIONID'] = {'name':'REGIONID', 'type':'string','width':32,'precision':0,'transfer':'constant','source':regionid }
        fieldDD['NAME'] = {'name':'NAME', 'type':'string','width':64,'precision':0,'transfer':'constant','source':regionname }
        fieldDD['CATEGORY'] = {'name':'CATEGORY', 'type':'string','width':32,'precision':0,'transfer':'constant','source':regioncat }
        fieldDD['STRATUM'] = {'name':'STRATUM', 'type':'integer','width':4,'precision':0,'transfer':'constant','source':stratum }
        fieldDD['PARENTID'] = {'name':'PARENTID', 'type':'string','width':32,'precision':0,'transfer':'constant','source':parentid }
        fieldDD['PARENTCAT'] = {'name':'PARENTCAT', 'type':'string','width':32,'precision':0,'transfer':'constant','source':parentcat }
        return fieldDD
