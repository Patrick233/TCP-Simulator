#Create a simulator object
set ns [new Simulator]

#Create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

set pkt_size [200]
set filename ["output/trace"]

#Open the trace file
set tf [open $filename w]
$ns trace-all $tf

#Create agents and applications
set udp0 [new Agent/UDP]
set null0 [new Agent/Null]
set tcp0 [new Agent/TCP]
set tcp0 [new Agent/TCP]

set tcpsink0 [new Agent/TCPSink]
set cbr0 [new Application/Traffic/CBR]
set ftp0 [new Application/FTP]

set tcpsink0 [new Agent/TCPSink]
set cbr0 [new Application/Traffic/CBR]
set ftp0 [new Application/FTP]

proc create_topology {} {
	global ns n1 n2 n3 n4 n5 n6

	$ns duplex-link $n1 $n2 10Mb 10ms DropTail
	$ns duplex-link $n2 $n5 10Mb 10ms DropTail
	$ns duplex-link $n2 $n3 10Mb 10ms DropTail
	$ns duplex-link $n3 $n4 10Mb 10ms DropTail
	$ns duplex-link $n3 $n6 10Mb 10ms DropTail
}

proc create_CBR {} {
	global ns n2 n3 udp0 null0 cbr0 pkt_size

	#Setup CBR over UDP connection
	$ns attach-agent $n2 $udp0
	$cbr0 attach-agent $udp0
	$cbr0 set type_ CBR
	$cbr0 set packet_size_ $pkt_size
	$cbr0 set rate_ 1mbs
	$cbr0 set random_ false
	$ns attach-agent $n3 $null0
	$ns connect $udp0 $null0
}

proc create_FTP {} {
	global ns n1 n4 tcp0 tcpsink0 ftp0

	$ns attach-agent $n1 $tcp0
	$ftp0 attach-agent $tcp0
	$ns attach-agent $n4 $tcpsink0
	$ns connect $tcp0 $tcpsink0
}

proc schedule {} {
	global ns cbr0 ftp0

	$ns at 0.1 "$cbr0 start"
	$ns at 1.0 "$ftp0 start"
	$ns at 55.0 "$cbr0 stop"
	$ns at 59.0 "$ftp0 stop"
	$ns at 60.0 "finish"
}

proc finish {} {
	global ns tf
	
	$ns flush-trace
	close $tf
	exit 0
}

create_topology
create_CBR
create_FTP
schedule

$ns run