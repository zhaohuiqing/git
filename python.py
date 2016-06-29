#encoding:utf-8
import os


# 获取当前设备id，并打印出来
def get_deviceId():
	devicesids = os.popen('adb devices ').read()
	devicesid = devicesids.split('\n')
	for index in range(1,len(devicesid)):
		if devicesid[index].find('device'):
			device = devicesid[index].strip(devicesid[index][-6:])
		return device


# 输入一个apk的绝对路径,分别输入包名和启动activity,并启动该app
def getApkInfo(filepath):
	
	#filepath = 'D:\git\\bigolive-1.2.0-SNAPSHOT-658-official.apk'
	cmd = "aapt dump badging "+ filepath
	infos = os.popen(cmd).readlines()
	for i in infos:
		if 'package' in i:
			start = i.find('\'')
			#print type(start)
			end = i.find('\'',start+1)
			#print type(end)
			packagename = i[start+1:end]
	for j in infos:
		if 'launchable-activity' in j:
			start = j.find('\'')
			#print type(start)
			end = j.find('\'',start+1)
			#print type(end)
			activity = j[start+1:end]

	return [packagename,activity]
	#os.system('adb shell am start -n com.yy.yymeet/com.yy.iheima.startup.SplashActivity')


#如果手机上已经有此app,则卸载,如果没有则安装
def reinstall(packagename,filepath,id):
	packages = os.popen('adb -s '+ id + ' shell pm list packages').read()
	if packages.find(packagename):
		cmd = "adb uninstall " + packagename
		os.popen(cmd)
		print packagename +'uninstall successed'
	else:
		print 'the phone does not install this apk,install it right now'
	cmd = 'adb -s '+ id +' install '+filepath
	os.system(cmd)

#如果手机上有此app则跳过，没有则重新安装
def install(packagename,filepath,id):
	packages = os.popen('adb -s '+ id + ' shell pm list packages').read()
	if packages.find(packagename):
		print 'this phone already install this app'
	else:
		print 'the phone does not install this apk,install it right now'
		cmd = 'adb -s '+ id +' install '+filepath
		os.system(cmd)


#根据包名和启动Activity启动app
def start(packagename,activity):
	cmd = 'adb shell am start -n '+ packagename +'/' + activity
	os.system(cmd)

#按home键返回，并杀进程
def  homeAndKill(packagename):
	os.system('adb shell input keyevent 3')
	cmd = 'adb shell am force-stop ' + packagename
	os.system(cmd)
# 截屏
def screenShot():

	os.system('adb shell /system/bin/screencap -p /sdcard/screenshot.png')
	os.system('adb pull /sdcard/screenshot.png  F:/test/python/screenshots ')




if __name__=='__main__':
	filepath = raw_input("输入要解析包的路径:")
	id = get_deviceId()
	apkinfo = getApkInfo(filepath)
	packagename = apkinfo[0]
	activity = apkinfo[1]
	install(packagename,filepath,id)

	#启动app，按home键返回桌面并杀进程
	start(packagename,activity)
	homeAndKill(packagename)


