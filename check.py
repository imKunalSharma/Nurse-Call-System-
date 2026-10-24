import alsaaudio



m = alsaaudio.Mixer()
vol = m.getvolume()
vol = int(vol[0])

newvol = vol -10
vol2 = m.setvolume(newvol)
print(vol)