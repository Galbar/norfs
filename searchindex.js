Search.setIndex({docnames:["examples","index","norfs","norfs.copy","norfs.fs"],envversion:53,filenames:["examples.rst","index.rst","norfs.rst","norfs.copy.rst","norfs.fs.rst"],objects:{"":{norfs:[2,0,0,"-"]},"norfs.Version":{MAJOR:[2,2,1,""],MINOR:[2,2,1,""],PATCH:[2,2,1,""],RELEASE:[2,2,1,""],VERSION:[2,2,1,""]},"norfs.copy":{CopyDirectory:[3,1,1,""],CopyError:[3,5,1,""],CopyFile:[3,1,1,""],CopyFileSystemObject:[3,1,1,""],CopyHandler:[3,1,1,""],GenericCopier:[3,1,1,""],local:[3,0,0,"-"],s3:[3,0,0,"-"]},"norfs.copy.CopyDirectory":{copy:[3,4,1,""],copy_from_dir:[3,4,1,""],copy_from_file:[3,4,1,""],file:[3,4,1,""],subdir:[3,4,1,""]},"norfs.copy.CopyFile":{copy:[3,4,1,""],copy_from_dir:[3,4,1,""],copy_from_file:[3,4,1,""]},"norfs.copy.CopyFileSystemObject":{copy:[3,4,1,""],copy_from_dir:[3,4,1,""],copy_from_file:[3,4,1,""],fs:[3,2,1,""],path:[3,2,1,""]},"norfs.copy.CopyHandler":{copy:[3,4,1,""],set_copy_policy:[3,4,1,""]},"norfs.copy.GenericCopier":{copy_dir_to_dir:[3,4,1,""],copy_file_to_file:[3,4,1,""]},"norfs.copy.local":{LocalToLocalCopier:[3,1,1,""],LocalToS3Copier:[3,1,1,""]},"norfs.copy.local.LocalToLocalCopier":{copy_file_to_file:[3,4,1,""]},"norfs.copy.local.LocalToS3Copier":{copy_file_to_file:[3,4,1,""]},"norfs.copy.s3":{S3ToLocalCopier:[3,1,1,""],S3ToS3Copier:[3,1,1,""]},"norfs.copy.s3.S3ToLocalCopier":{copy_file_to_file:[3,4,1,""]},"norfs.copy.s3.S3ToS3Copier":{copy_dir_to_dir:[3,4,1,""],copy_file_to_file:[3,4,1,""]},"norfs.filesystem":{BaseFileSystemObject:[2,1,1,""],Directory:[2,1,1,""],File:[2,1,1,""]},"norfs.filesystem.BaseFileSystemObject":{as_dir:[2,4,1,""],as_file:[2,4,1,""],copy:[2,4,1,""],exists:[2,4,1,""],is_dir:[2,4,1,""],is_file:[2,4,1,""],name:[2,2,1,""],parent:[2,4,1,""],path:[2,2,1,""],remove:[2,4,1,""],uri:[2,2,1,""]},"norfs.filesystem.Directory":{as_dir:[2,4,1,""],file:[2,4,1,""],is_dir:[2,4,1,""],list:[2,4,1,""],remove:[2,4,1,""],subdir:[2,4,1,""]},"norfs.filesystem.File":{as_file:[2,4,1,""],is_file:[2,4,1,""],read:[2,4,1,""],remove:[2,4,1,""],write:[2,4,1,""]},"norfs.fs":{BaseFileSystem:[4,1,1,""],DirListResult:[4,1,1,""],FileSystemOperationError:[4,5,1,""],NotAFileError:[4,5,1,""],Path:[4,1,1,""],local:[4,0,0,"-"],memory:[4,0,0,"-"],s3:[4,0,0,"-"]},"norfs.fs.BaseFileSystem":{ERROR_MESSAGE:[4,2,1,""],dir_list:[4,4,1,""],dir_remove:[4,4,1,""],file_read:[4,4,1,""],file_remove:[4,4,1,""],file_write:[4,4,1,""],parse_path:[4,4,1,""],path_exists:[4,4,1,""],path_to_string:[4,4,1,""],path_to_uri:[4,4,1,""]},"norfs.fs.DirListResult":{dirs:[4,2,1,""],files:[4,2,1,""],others:[4,2,1,""]},"norfs.fs.Path":{basename:[4,2,1,""],child:[4,4,1,""],drive:[4,2,1,""],parent:[4,2,1,""],tail:[4,2,1,""]},"norfs.fs.local":{LocalFileSystem:[4,1,1,""]},"norfs.fs.local.LocalFileSystem":{dir_list:[4,4,1,""],dir_remove:[4,4,1,""],file_read:[4,4,1,""],file_remove:[4,4,1,""],file_write:[4,4,1,""],parse_path:[4,4,1,""],path_exists:[4,4,1,""],path_to_string:[4,4,1,""],path_to_uri:[4,4,1,""]},"norfs.fs.memory":{MemoryDirectory:[4,1,1,""],MemoryFile:[4,1,1,""],MemoryFileSystem:[4,1,1,""]},"norfs.fs.memory.MemoryDirectory":{get_dir:[4,4,1,""],get_file:[4,4,1,""],list_dirs:[4,4,1,""],list_files:[4,4,1,""],put_dir:[4,4,1,""],put_file:[4,4,1,""],remove_dir:[4,4,1,""],remove_file:[4,4,1,""]},"norfs.fs.memory.MemoryFile":{contents:[4,2,1,""]},"norfs.fs.memory.MemoryFileSystem":{dir_list:[4,4,1,""],dir_remove:[4,4,1,""],file_read:[4,4,1,""],file_remove:[4,4,1,""],file_write:[4,4,1,""],parse_path:[4,4,1,""],path_exists:[4,4,1,""],path_to_string:[4,4,1,""],path_to_uri:[4,4,1,""]},"norfs.fs.s3":{S3FileSystem:[4,1,1,""]},"norfs.fs.s3.S3FileSystem":{dir_list:[4,4,1,""],dir_remove:[4,4,1,""],file_read:[4,4,1,""],file_remove:[4,4,1,""],file_write:[4,4,1,""],parse_path:[4,4,1,""],path_exists:[4,4,1,""],path_to_string:[4,4,1,""],path_to_uri:[4,4,1,""]},norfs:{Version:[2,1,1,""],configure:[2,3,1,""],copy:[3,0,0,"-"],filesystem:[2,0,0,"-"],fs:[4,0,0,"-"],get_copy_handler:[2,3,1,""],get_local_fs:[2,3,1,""],get_memory_fs:[2,3,1,""],get_s3_fs:[2,3,1,""],localdir:[2,3,1,""],localfile:[2,3,1,""],memorydir:[2,3,1,""],memoryfile:[2,3,1,""],s3dir:[2,3,1,""],s3file:[2,3,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","function","Python function"],"4":["py","method","Python method"],"5":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:function","4":"py:method","5":"py:exception"},terms:{"abstract":1,"byte":[2,4],"class":[2,3,4],"default":2,"import":[0,1],"new":1,"public":1,"return":[1,2],The:2,_path:2,absolut:[1,2],accept:2,also:1,ani:[1,2,3,4],as_dir:2,as_fil:2,assert:0,base:[2,3,4],basefilesystem:[2,3,4],basefilesystemobject:2,basenam:4,being:[1,2],bool:[2,4],boto3:[0,1,2],bucket:2,can:1,child:4,client:[0,1,2],code:1,common:1,compat:1,configur:[0,1,2],content:0,contract:1,copi:2,copier:3,copy_dir_to_dir:3,copy_file_to_fil:3,copy_from_dir:3,copy_from_fil:3,copy_handl:2,copydirectori:3,copyerror:3,copyfil:3,copyfilesystemobject:3,copyhandl:[2,3],creat:[1,2],current:2,default_copi:3,destin:2,dir:4,dir_:4,dir_list:4,dir_remov:4,directori:2,dirlistresult:4,doe:[1,2],download:1,drive:4,dst:3,dst_f:3,easili:1,empti:[1,2],error_messag:4,everyth:2,except:[3,4],exist:2,expos:1,extend:1,extens:1,fail:[1,2],failur:[1,2],file:[2,3,4],file_:4,file_read:4,file_remov:4,file_writ:4,filesystemoperationerror:[1,2,4],first:2,follow:1,from:[1,2],full:[1,2],genericcopi:3,get_copy_handl:2,get_dir:4,get_fil:4,get_local_f:2,get_memory_f:2,get_s3_f:2,git:1,given:[1,2],global:2,ile:1,implement:[1,4],index:1,instanc:[1,2],interact:1,is_dir:2,is_fil:2,issu:1,its:[1,2],itself:[1,2],keyword:2,kwarg:2,librari:[1,2],list:[2,4],list_dir:4,list_fil:4,local:2,local_fil:0,localdir:[1,2],localfil:[0,1,2],localfilesystem:[2,4],localtolocalcopi:3,localtos3copi:3,major:2,maliz:1,memori:2,memory_separ:2,memorydir:[1,2],memorydirectori:4,memoryfil:[1,2,4],memoryfilesystem:[2,4],minor:2,modul:1,most:1,multipl:1,my_directori:1,my_fil:1,mybucket:[0,1],mydir:0,name:[2,4],none:[2,3,4],nonetyp:2,nor:1,norf:0,notadirectoryerror:[1,2],notafileerror:[1,2,4],object:[1,2,3,4],offer:1,one:2,onli:2,oper:4,other:4,page:1,paramet:2,parent:[2,4],parse_path:4,patch:2,path:[2,3,4],path_exist:4,path_or_bucket:2,path_str:2,path_to_str:4,path_to_uri:4,pip:1,point:[1,2],prefix:2,protocol:2,put_dir:4,put_fil:4,rais:[1,2],read:[0,2],rel:[1,2],releas:2,remot:1,remov:2,remove_dir:4,remove_fil:4,repositori:1,repres:1,represent:1,root:4,s3_client:[0,1,2,3,4],s3_dir:0,s3_protocol:2,s3_separ:2,s3dir:[0,1,2],s3file:[1,2],s3filesystem:[2,4],s3tolocalcopi:3,s3tos3copi:3,search:1,self:[1,2],separ:[2,4],set:[1,2],set_copy_polici:3,simpl:1,some:0,sourc:[1,2,3,4],special:1,src:3,src_f:3,store:1,str:[2,3,4],subclass:1,subdir:[2,3],suffix:3,system:[1,2],tail:4,thi:[1,2],tri:[1,2],txt:[0,1],type:[2,3,4],typeerror:1,union:2,uri:2,uri_protocol:4,use:2,valu:2,veri:1,version:2,want:1,wether:2,whether:[1,2],work:1,write:[0,2],you:1,yourself:1,ystem:1},titles:["Examples","norfs","norfs package","norfs.copy package","norfs.fs package"],titleterms:{"byte":1,The:1,as_dir:1,as_fil:1,basefilesystemobject:1,bool:1,content:[1,2,3,4],copi:[0,1,3],destin:1,directori:1,exampl:0,exist:1,file:[0,1],filesystem:[1,2],indic:1,instal:1,interfac:1,is_dir:1,is_fil:1,list:1,local:[0,1,3,4],memori:[1,4],modul:[2,3,4],name:1,none:1,norf:[1,2,3,4],packag:[2,3,4],parent:1,path:1,read:1,remov:1,str:1,subdir:1,submodul:[2,3,4],subpackag:2,support:1,tabl:1,uri:1,write:1}})