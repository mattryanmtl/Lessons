require 'date'

def calendar(year, month)
  s = []
  date = DateTime.new(year, month)
  monthname = DateTime::MONTHNAMES[month]

  s << "<table>"
  s << "<caption>#{monthname}</caption>"
  s << "<tr><th>M<th>T<th>W<th>T<th>F<th>S<th>S"
  s << "<tr>" + "<td>" * (date.cwday - 1)

  begin
    s << "<tr>" if date.monday?
    s << "<td>#{date.day}"
    date += 1
  end while date.day != 1
  s << "</table>"
  s.join
end

puts DATA.read
puts "<table>"
(0..3).each do |i|
  puts "<tr>"
  (0..2).each do |j|
    puts "<td class='big'>"
    puts calendar(2012, i * 3 + j + 1)
  end
end

__END__
<html>
<head>
<style type="text/css">
td.big { border:1px solid black; }
td     { vertical-align:top; }
</style>
</head>
<body>
<h1>2012 calendar</h1>
