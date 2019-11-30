from firmUpdater import *

# starting everything
app = Application()
app.add_service(FirmwareUpdateService(0))
app.add_service(FirmwareUpdateService2(3))
localmac = app.register()
adv = Pi0Advertisement(0, localmac)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
except:
    traceback.print_exc()
    e = sys.exc_info()[0]
    print("Error: %s" % e)