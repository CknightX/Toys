package main

import (
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"sync"
)

func get_http_client(is_proxy bool, proxy_address string) *http.Client {
	client := &http.Client{}
	if is_proxy {
		proxy := func(*http.Request) (*url.URL, error) {
			return url.Parse("http://" + proxy_address)
		}
		transport := &http.Transport{Proxy: proxy}
		client = &http.Client{Transport: transport}
	}
	return client
}

func get_html(url string, client *http.Client) string {

	req, _ := http.NewRequest("GET", url, nil)

	resp, err := client.Do(req)
	if err != nil {
		return ""
	}
	if resp.StatusCode != 200 {
		return ""
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return ""
	}
	return string(body)
}

func parse_image_url(source_html string) string {
	reg := regexp.MustCompile(`original":"(.+?)"`)
	result := reg.FindStringSubmatch(source_html)
	if len(result) == 0 {
		return ""
	}
	return result[1]

}

func download_img(img_url string, file_name string, client *http.Client) {
	req, err := http.NewRequest("GET", img_url, nil)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("authority", "i.pximg.net")
	req.Header.Set("pragma", "no-cache")
	req.Header.Set("cache-control", "no-cache")
	req.Header.Set("sec-ch-ua", `^\^`)
	req.Header.Set("sec-ch-ua-mobile", "?0")
	req.Header.Set("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
	req.Header.Set("accept", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8")
	req.Header.Set("sec-fetch-site", "cross-site")
	req.Header.Set("sec-fetch-mode", "no-cors")
	req.Header.Set("sec-fetch-dest", "image")
	req.Header.Set("referer", "https://www.pixiv.net/")
	req.Header.Set("accept-language", "zh-CN,zh;q=0.9")
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	f, err := os.Create(file_name)
	if f != nil {
		defer f.Close()
	}
	if err != nil {
		panic(err)
	}
	io.Copy(f, resp.Body)
}
func worker(img_ID string, client *http.Client, wg *sync.WaitGroup) {
	defer wg.Done()
	img_url := "https://www.pixiv.net/artworks/" + img_ID
	html := get_html(img_url, client)
	image_url := parse_image_url(html)
	download_img(image_url, img_ID+".jpg", client)
	log.Printf("ID:%v Downloaded\n", img_ID)
}

func main() {
	wg := &sync.WaitGroup{}
	client := get_http_client(true, "127.0.0.1:7890")
	img_nums := len(os.Args) - 1
	if img_nums == 0 {
		log.Fatal("too few params")
	}
	for i := 1; i <= img_nums; i++ {
		wg.Add(1)
		go worker(os.Args[i], client, wg)
	}
	wg.Wait()
}
