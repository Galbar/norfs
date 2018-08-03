Search.setIndex({docnames:["examples","index","norfs","norfs.copy","norfs.fs"],envversion:53,filenames:["examples.rst","index.rst","norfs.rst","norfs.copy.rst","norfs.fs.rst"],objects:{"":{norfs:[2,0,0,"-"]},"norfs.Version":{MAJOR:[2,2,1,""],MINOR:[2,2,1,""],PATCH:[2,2,1,""],RELEASE:[2,2,1,""],VERSION:[2,2,1,""]},"norfs.client":{CopyClient:[2,1,1,""],FileSystemClient:[2,1,1,""]},"norfs.client.CopyClient":{copier:[2,2,1,""],copy:[2,3,1,""]},"norfs.client.FileSystemClient":{dir:[2,3,1,""],file:[2,3,1,""],fs:[2,2,1,""]},"norfs.copy":{base:[3,0,0,"-"],local:[3,0,0,"-"],s3:[3,0,0,"-"]},"norfs.copy.base":{Copier:[3,1,1,""],CopyDirectory:[3,1,1,""],CopyError:[3,4,1,""],CopyFile:[3,1,1,""],CopyFileSystemObject:[3,1,1,""],CopyStrategy:[3,1,1,""],GenericCopyStrategy:[3,1,1,""]},"norfs.copy.base.Copier":{copy:[3,3,1,""],set_copy_policy:[3,3,1,""]},"norfs.copy.base.CopyDirectory":{copy:[3,3,1,""],copy_from_dir:[3,3,1,""],copy_from_file:[3,3,1,""],file:[3,3,1,""],subdir:[3,3,1,""]},"norfs.copy.base.CopyFile":{copy:[3,3,1,""],copy_from_dir:[3,3,1,""],copy_from_file:[3,3,1,""]},"norfs.copy.base.CopyFileSystemObject":{copy:[3,3,1,""],copy_from_dir:[3,3,1,""],copy_from_file:[3,3,1,""],fs:[3,2,1,""],path:[3,2,1,""]},"norfs.copy.base.CopyStrategy":{copy_dir_to_dir:[3,3,1,""],copy_file_to_file:[3,3,1,""]},"norfs.copy.base.GenericCopyStrategy":{copy_dir_to_dir:[3,3,1,""],copy_file_to_file:[3,3,1,""]},"norfs.copy.local":{LocalToLocalCopyStrategy:[3,1,1,""],LocalToS3CopyStrategy:[3,1,1,""]},"norfs.copy.local.LocalToLocalCopyStrategy":{copy_file_to_file:[3,3,1,""]},"norfs.copy.local.LocalToS3CopyStrategy":{copy_file_to_file:[3,3,1,""]},"norfs.copy.s3":{S3ToLocalCopyStrategy:[3,1,1,""],S3ToS3CopyStrategy:[3,1,1,""]},"norfs.copy.s3.S3ToLocalCopyStrategy":{copy_file_to_file:[3,3,1,""]},"norfs.copy.s3.S3ToS3CopyStrategy":{copy_dir_to_dir:[3,3,1,""],copy_file_to_file:[3,3,1,""]},"norfs.filesystem":{BaseFileSystemObject:[2,1,1,""],Directory:[2,1,1,""],File:[2,1,1,""]},"norfs.filesystem.BaseFileSystemObject":{as_dir:[2,3,1,""],as_file:[2,3,1,""],copy_object:[2,3,1,""],exists:[2,3,1,""],is_dir:[2,3,1,""],is_file:[2,3,1,""],name:[2,2,1,""],parent:[2,3,1,""],path:[2,2,1,""],remove:[2,3,1,""],uri:[2,2,1,""]},"norfs.filesystem.Directory":{as_dir:[2,3,1,""],copy_object:[2,3,1,""],file:[2,3,1,""],is_dir:[2,3,1,""],list:[2,3,1,""],remove:[2,3,1,""],subdir:[2,3,1,""]},"norfs.filesystem.File":{as_file:[2,3,1,""],copy_object:[2,3,1,""],is_file:[2,3,1,""],read:[2,3,1,""],remove:[2,3,1,""],write:[2,3,1,""]},"norfs.fs":{base:[4,0,0,"-"],local:[4,0,0,"-"],memory:[4,0,0,"-"],s3:[4,0,0,"-"]},"norfs.fs.base":{BaseFileSystem:[4,1,1,""],DirListResult:[4,1,1,""],FileSystemOperationError:[4,4,1,""],NotAFileError:[4,4,1,""],Path:[4,1,1,""]},"norfs.fs.base.BaseFileSystem":{ERROR_MESSAGE:[4,2,1,""],dir_list:[4,3,1,""],dir_remove:[4,3,1,""],file_read:[4,3,1,""],file_remove:[4,3,1,""],file_write:[4,3,1,""],parse_path:[4,3,1,""],path_exists:[4,3,1,""],path_to_string:[4,3,1,""],path_to_uri:[4,3,1,""]},"norfs.fs.base.DirListResult":{dirs:[4,2,1,""],files:[4,2,1,""],others:[4,2,1,""]},"norfs.fs.base.Path":{basename:[4,2,1,""],child:[4,3,1,""],drive:[4,2,1,""],parent:[4,2,1,""],tail:[4,2,1,""]},"norfs.fs.local":{LocalFileSystem:[4,1,1,""]},"norfs.fs.local.LocalFileSystem":{dir_list:[4,3,1,""],dir_remove:[4,3,1,""],file_read:[4,3,1,""],file_remove:[4,3,1,""],file_write:[4,3,1,""],parse_path:[4,3,1,""],path_exists:[4,3,1,""],path_to_string:[4,3,1,""],path_to_uri:[4,3,1,""]},"norfs.fs.memory":{MemoryDirectory:[4,1,1,""],MemoryFile:[4,1,1,""],MemoryFileSystem:[4,1,1,""]},"norfs.fs.memory.MemoryDirectory":{get_dir:[4,3,1,""],get_file:[4,3,1,""],list_dirs:[4,3,1,""],list_files:[4,3,1,""],put_dir:[4,3,1,""],put_file:[4,3,1,""],remove_dir:[4,3,1,""],remove_file:[4,3,1,""]},"norfs.fs.memory.MemoryFile":{contents:[4,2,1,""]},"norfs.fs.memory.MemoryFileSystem":{dir_list:[4,3,1,""],dir_remove:[4,3,1,""],file_read:[4,3,1,""],file_remove:[4,3,1,""],file_write:[4,3,1,""],parse_path:[4,3,1,""],path_exists:[4,3,1,""],path_to_string:[4,3,1,""],path_to_uri:[4,3,1,""]},"norfs.fs.s3":{S3FileSystem:[4,1,1,""]},"norfs.fs.s3.S3FileSystem":{dir_list:[4,3,1,""],dir_remove:[4,3,1,""],file_read:[4,3,1,""],file_remove:[4,3,1,""],file_write:[4,3,1,""],parse_path:[4,3,1,""],path_exists:[4,3,1,""],path_to_string:[4,3,1,""],path_to_uri:[4,3,1,""]},"norfs.helpers":{get_copy_client:[2,5,1,""],local:[2,5,1,""],memory:[2,5,1,""],s3:[2,5,1,""]},norfs:{Version:[2,1,1,""],client:[2,0,0,"-"],copy:[3,0,0,"-"],filesystem:[2,0,0,"-"],fs:[4,0,0,"-"],helpers:[2,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","exception","Python exception"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:exception","5":"py:function"},terms:{"abstract":1,"byte":[2,4],"class":[1,2,3,4],"import":[0,1],"new":1,"public":1,"return":[1,2],The:2,_path:2,absolut:[1,2],access:1,also:1,ani:[1,3,4],api:1,arg:2,as_dir:2,as_fil:2,assert:0,base:2,basefilesystem:[2,3,4],basefilesystemobject:2,basenam:4,being:[1,2],better:1,between:1,bool:[2,4],both:1,boto3:[0,1],can:1,child:4,client:[0,1],code:1,common:1,compat:1,compos:1,configur:1,content:0,contract:1,copi:2,copier:[2,3],copy_dir_to_dir:3,copy_file_to_fil:3,copy_from_dir:3,copy_from_fil:3,copy_object:2,copy_strategi:3,copycli:2,copydirectori:3,copyerror:3,copyfil:3,copyfilesystemobject:[2,3],copystrategi:3,cp_for_al:1,cp_local_onli:1,creat:[1,2],current:2,default_copy_strategi:3,demo:1,demo_fil:1,destin:1,dir:[0,2,4],dir_:4,dir_list:4,dir_remov:4,directori:2,dirlistresult:4,doe:[1,2],download:1,drive:4,dst:[2,3],dst_f:3,each:1,easi:1,easili:1,empti:[1,2],error_messag:4,except:[3,4],exist:2,expos:1,extend:1,extens:1,fail:[1,2],failur:[1,2],file:[2,3,4],file_:4,file_read:4,file_remov:4,file_writ:4,filesystemcli:2,filesystemoperationerror:[1,2,4],follow:1,from:[1,2],full:[1,2],genericcopystrategi:3,get_copy_cli:[0,1,2],get_dir:4,get_fil:4,git:1,given:[1,2],handi:1,have:1,hello:1,help:1,helper:[0,1],ile:1,implement:[1,4],index:1,instanc:[1,2],interact:1,is_dir:2,is_fil:2,issu:1,its:[1,2],itself:[1,2],kwarg:2,librari:1,list:[2,4],list_dir:4,list_fil:4,local:2,local_fil:0,local_fs_cli:1,localfilesystem:4,localtolocalcopystrategi:3,localtos3copystrategi:3,major:2,make:1,maliz:1,manag:1,mater:1,memori:2,memory_fs_cli:1,memorydirectori:4,memoryfil:4,memoryfilesystem:4,minor:2,modul:1,most:1,multipl:1,my_directori:1,my_fil:1,mybucket:[0,1],mydir:0,name:[2,4],none:[2,3,4],nonetyp:2,nor:1,norf:0,notadirectoryerror:[1,2],notafileerror:[1,2,4],object:[1,2,3,4],obtain:1,offer:1,onli:1,oper:[1,4],other:4,page:1,pair:1,parent:[2,4],parse_path:4,pass:1,patch:2,path:[2,3,4],path_exist:4,path_str:2,path_to_str:4,path_to_uri:4,pip:1,point:[1,2],polici:1,print:1,provid:1,put_dir:4,put_fil:4,rais:[1,2],read:[0,2],rel:[1,2],releas:2,remot:1,remov:2,remove_dir:4,remove_fil:4,repositori:1,repres:1,represent:1,root:4,s3_client:[0,1,3,4],s3_dir:0,s3_fs_client:1,s3filesystem:4,s3tolocalcopystrategi:3,s3tos3copystrategi:3,search:1,self:[1,2],sens:1,separ:4,set:[1,2],set_copy_polici:3,simpl:1,some:0,sourc:[1,2,3,4],source_fil:1,special:1,src:[2,3],src_f:3,store:1,str:[2,3,4],strategi:1,subclass:1,subdir:[2,3],suffix:3,system:[1,2],tail:4,target_fil:1,than:1,thei:1,them:1,thi:1,tri:[1,2],txt:[0,1],typeerror:1,unifi:1,union:2,uri:2,uri_protocol:4,using:1,usual:1,veri:1,version:2,wai:1,want:1,wether:2,whether:[1,2],work:1,world:1,write:[0,2],you:1,yourself:1,ystem:1},titles:["Examples","norfs","norfs package","norfs.copy package","norfs.fs package"],titleterms:{"byte":1,The:1,as_dir:1,as_fil:1,base:[1,3,4],basefilesystem:1,basefilesystemobject:1,bool:1,client:2,content:[1,2,3,4],copi:[0,1,3],copier:1,copycli:1,dir:1,directori:1,dst:1,exampl:0,exist:1,file:[0,1],filesystem:[1,2],filesystemcli:1,helper:2,indic:1,instal:1,interfac:1,is_dir:1,is_fil:1,list:1,local:[0,1,3,4],memori:[1,4],modul:[2,3,4],name:1,none:1,norf:[1,2,3,4],packag:[2,3,4],parent:1,path:1,read:1,remov:1,src:1,str:1,subdir:1,submodul:[2,3,4],subpackag:2,support:1,tabl:1,uri:1,write:1}})