FROM archlinux:base-devel

RUN sed -i 's/#DisableSandbox/DisableSandbox/' /etc/pacman.conf 
# This is nessecary.
RUN pacman -Sy
RUN pacman -S python python-pyinotify --noconfirm

RUN useradd builder && passwd -d builder && printf 'builder ALL=(ALL) ALL\n' | tee -a /etc/sudoers

USER builder:builder

VOLUME [ "/data" ]
WORKDIR /data

RUN chown -R builder:builder /data

COPY entrypoint.py /entrypoint.py

EXPOSE 8000

CMD [ "/usr/bin/python", "/entrypoint.py" ]
