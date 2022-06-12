import PhotoScan

chunk=Metashape.app.document.chunks[0]
my_list=[]

with open ('/Users/domidenunzio/Desktop/metashape_prueba.txt','w') as f:
        f.write('camera'+'\t'+'target'+'\t'+'\t'+'x'+'\t'+'y'+'\n')
        for camera in chunk.cameras:
                
                for marker in chunk.markers:
                        if not marker.projections[camera]:
                                continue
                        else:
                                x0, y0 = marker.projections[camera].coord
                                markerstr=str(marker.label).split(' ')
                                markerstr=markerstr[-1]
                                print(camera.label,'\t',marker.label,'\t',x0,'\t',y0)
                                f.write(str(camera.label)+'\t'+markerstr+'\t'+str(x0)+'\t'+str(y0)+'\n')
